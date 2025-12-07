from abc import abstractmethod, ABC
from collections import Counter
from datetime import datetime, timedelta, time

from sqlalchemy.ext.asyncio import AsyncSession

from backend.entity.booking import BookingEntity
from backend.entity.service import ServiceEntity
from backend.repository.booking_repository import IBookingRepository
from backend.repository.company_repository import ICompanyRepository
from backend.repository.service_repository import IServiceRepository
from backend.core.config import CalendarSchedule


class IBookingUseCase(ABC):

    @abstractmethod
    async def save_booking(
            self,
            session: AsyncSession,
            service_id: int,
            client_id: int,
            time_start: datetime,
            time_end: datetime):
        raise NotImplemented

    @abstractmethod
    async def get_booking_by_id(self, session: AsyncSession, service_id: int, company_id: int, work_schedule: list):
        raise NotImplemented

    @abstractmethod
    async def get_booking_by_client(self, session: AsyncSession, client_id: int) -> list[BookingEntity] | None:
        raise NotImplemented

    @abstractmethod
    async def get_booking_by_service_id_and_client_id(
            self,
            session: AsyncSession,
            service_id: int,
            client_id: int
    ) -> BookingEntity | None:
        raise NotImplemented


class BookingUseCase(IBookingUseCase):

    def __init__(
            self,
            booking_repository: IBookingRepository,
            service_repository: IServiceRepository,
            company_repository: ICompanyRepository,
            calendar_schedule_settings: CalendarSchedule
    ):
        self.service_repository = service_repository
        self.company_repository = company_repository
        self.calendar_schedule_settings = calendar_schedule_settings
        self.booking_repository = booking_repository

    async def save_booking(
            self,
            session: AsyncSession,
            service_id: int,
            client_id: int,
            time_start: datetime,
            time_end: datetime):
        return await self.booking_repository.save_booking(session, service_id, client_id, time_start, time_end)

    @staticmethod
    def get_work_schedule_by_day_of_week(work_schedule, day_of_week: int):
        for ws in work_schedule:
            if ws["day_of_week"] == day_of_week:
                return ws

    @staticmethod
    def get_intervals(
            start_time: time,
            end_time: time,
            service_duration_min: int
    ) -> list[tuple[time, time]]:

        if end_time <= start_time:
            raise ValueError("end_time должно быть строго позже start_time")
        if service_duration_min <= 0:
            raise ValueError("Длительность услуги должна быть положительной")

        # Переводим start_time и end_time в объекты datetime для удобства арифметики
        # Берём произвольную дату (например, сегодня), чтобы работать с datetime
        today = datetime.now().date()
        start_dt = datetime.combine(today, start_time)
        end_dt = datetime.combine(today, end_time)

        intervals = []
        current_time = start_dt

        while current_time + timedelta(minutes=service_duration_min) <= end_dt:
            # Формируем интервал: от current_time до current_time + длительность
            end_interval = current_time + timedelta(minutes=service_duration_min)
            # Формат строки: "ЧЧ:ММ–ЧЧ:ММ"
            # interval_str = current_time.strftime("%H:%M") + "–" + end_interval.strftime("%H:%M")
            intervals.append((current_time.time(), end_interval.time()))
            # Переходим к следующему интервалу
            current_time = end_interval

        return intervals

    @staticmethod
    async def select_non_overlapping_intervals(intervals):
        if not intervals:
            return []

        intervals = [(time(start.hour, start.minute), time(end.hour, end.minute)) for start, end in intervals]

        # Считаем количество вхождений каждого кортежа
        counts = Counter(intervals)

        # Оставляем только кортежи с количеством = 1
        intervals = [item for item, count in counts.items() if count == 1]

        # Сортируем по времени окончания (жадный алгоритм)
        sorted_intervals = sorted(intervals, key=lambda x: x[1])

        selected = [sorted_intervals[0]]  # берём первый (самый ранний по окончанию)

        for current in sorted_intervals[1:]:
            last_selected = selected[-1]
            # Если текущий интервал начинается после окончания последнего выбранного
            if current[0] >= last_selected[1]:
                selected.append(current)

        return selected

    async def get_services_intervals(self, services: list[ServiceEntity], work_schedule: list) -> list[
        tuple[time, time]]:

        intervals = []

        for ws in work_schedule:
            work_start = datetime.strptime(ws.get("work_start"), "%H:%M").time()
            work_end = datetime.strptime(ws.get("work_end"), "%H:%M").time()
            for service in services:
                list_intervals = self.get_intervals(work_start, work_end, service.duration)
                intervals.extend(list_intervals)

        return intervals

    @staticmethod
    async def filter_intervals_by_service_duration(
            intervals: list[tuple[time, time]], service_duration_min: int
    ) -> list[dict[str, str]]:

        if service_duration_min <= 0:
            raise ValueError("Длительность услуги должна быть положительной")

        result = []

        for start, end in intervals:
            # Преобразуем time в datetime для арифметики (берём произвольную дату)
            dummy_date = datetime.now().date()  # можно любую дату
            start_dt = datetime.combine(dummy_date, start)
            end_dt = datetime.combine(dummy_date, end)

            # Проверяем, что конец >= начало
            if end_dt < start_dt:
                raise ValueError(f"Некорректный интервал: {start}–{end} (конец раньше начала)")

            # Вычисляем длительность интервала в минутах
            duration = (end_dt - start_dt).total_seconds() / 60

            # Если длительность точно равна заданной — добавляем в результат
            if duration == service_duration_min:
                result.append({
                    "start": start.strftime("%H:%M"),
                    "end": end.strftime("%H:%M"),
                })

        return result

    async def get_booking_by_id(self, session: AsyncSession, service_id: int, company_id: int, work_schedule: list):

        schedule: list[dict] = []

        service = await self.service_repository.get_service_by_id(session, service_id)
        if service is None:
            return

        services = await self.service_repository.get_services_by_company_id(session, company_id=company_id)

        days_of_week_to_work = {w["day_of_week"] for w in work_schedule}

        services_intervals = await self.get_services_intervals(services, work_schedule)

        bookings_by_service_id = await self.booking_repository.get_booking_by_service_id(session, service_id)

        bookings_intervals = [(t.time_start.time(), t.time_end.time(),) for t in bookings_by_service_id if t.client_id is not None]

        services_intervals.extend(bookings_intervals)

        non_overlapping_intervals = await self.select_non_overlapping_intervals(services_intervals)

        for day in range(self.calendar_schedule_settings.calendar_schedule_limit_days):
            now = datetime.now() + timedelta(days=day)
            if now.isoweekday() in days_of_week_to_work:

                time_to_book = await self.filter_intervals_by_service_duration(non_overlapping_intervals,
                                                                               service.duration),

                schedule.append({
                    "month": now.month,
                    "day": now.day,
                    "day_of_week": now.isoweekday(),
                    "time_to_book": time_to_book,
                    "is_work": True
                })
            else:
                schedule.append({
                    "month": now.month,
                    "day": now.day,
                    "day_of_week": now.isoweekday(),
                    "time_to_book": [],
                    "is_work": False
                })

        return {
            **service.to_dict(),
            "schedule": schedule
        }

    async def get_booking_by_client(self, session: AsyncSession, client_id: int) -> list[BookingEntity] | None:
        return await self.booking_repository.get_booking_by_client(session, client_id)

    async def get_booking_by_service_id_and_client_id(
            self,
            session: AsyncSession,
            service_id: int,
            client_id: int
    ) -> BookingEntity | None:
        return await self.booking_repository.get_booking_by_service_id_and_client_id(session, service_id, client_id)
