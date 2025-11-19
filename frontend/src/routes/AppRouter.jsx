import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "../pages/AuthPages/LoginPage/LoginPage.jsx";
import RegisterPage from "../pages/AuthPages/RegisterPage/RegisterPage.jsx";
import ForgotPasswordPage from "../pages/AuthPages/ForgotPasswordPage/ForgotPasswordPage.jsx";
import HomePage from "../pages/HomePage/HomePage.jsx";
import CompanyRecordsPage from "../pages/CompanyRecordsPage/CompanyRecordsPage.jsx";
import SchedulePage from "../pages/SchedulePage/SchedulePage.jsx"; 
import ServicesPage from "../pages/ServicesPage/ServicesPage.jsx";
import CompanySettingsPage from "../pages/CompanySettingsPage/CompanySettingsPage.jsx";
import PrivateRoute from "./PrivateRoute.jsx";

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Главная страница */}
        <Route path="/" element={<HomePage />} />

        {/* Авторизация */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
         {/* Расписание */}
        <Route path="/schedule" element={<SchedulePage />} />
        
        {/* Услуги */}
        <Route path="/services" element={<ServicesPage />} />
        
        {/* Настройки компании */}
        <Route path="/settings" element={<CompanySettingsPage />} />

        {/* Записи в компанию — только для авторизованных */}
        <Route
          path="/records"
          element={
            <PrivateRoute>
              <CompanyRecordsPage />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRouter;