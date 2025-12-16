@router.post(
    "/deactivate",
    responses={
        status.HTTP_200_OK: {"model": CompanySuccessResponse},
        status.HTTP_404_NOT_FOUND: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    }
)
async def deactivate_company(
        company=Depends(get_current_company_from_token),
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        await company_use_case.deactivate_company(session, company.id)
    except Exception as ex:
        logger.error(
            "Error occurred while deactivating company. Company id: %s Error: %s",
            company.id,
            str(ex),
            exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                error="Failed to deactivate company"
            ).model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanySuccessResponse(
            message="Company deactivated successfully"
        ).model_dump()
    )
