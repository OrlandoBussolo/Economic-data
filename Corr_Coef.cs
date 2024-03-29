Corr_Coef = 
VAR CurrentX = SELECTEDVALUE(Kpi_list[Value])
VAR CurrentY = SELECTEDVALUE(Kpi_list_2[Value])
VAR X_Column = SELECTCOLUMNS(kpi_sumarized, "X", 
                SWITCH(CurrentX,
                    "BBAS3", [BBAS3],
                    "BBDC4", [BBDC4],
                    "BPAC11", [BPAC11],
                    "INBR32", [INBR32],
                    "ITUB3", [ITUB3],
                    "ROXO34", [ROXO34],
                    "SANB11", [SANB11]
                )
            )
VAR Y_Column = SELECTCOLUMNS(kpi_sumarized, "Y", 
                SWITCH(CurrentY,
                    "BBAS3", [BBAS3],
                    "BBDC4", [BBDC4],
                    "BPAC11", [BPAC11],
                    "INBR32", [INBR32],
                    "ITUB3", [ITUB3],
                    "ROXO34", [ROXO34],
                    "SANB11", [SANB11]
                )
            )
VAR Corr_Coef_XY = SUMX(FILTER(ADDXATABLE(X_Column,Y_Column),ISNUMBER([X])&&ISNUMBER([Y])), [X]*[Y])
VAR Corr_Coef_X = SUMX(FILTER(ADDXATABLE(X_Column,Y_Column),ISNUMBER([X])&&ISNUMBER([Y])), [X])
VAR Corr_Coef_Y = SUMX(FILTER(ADDXATABLE(X_Column,Y_Column),ISNUMBER([X])&&ISNUMBER([Y])), [Y])
VAR Corr_Coef_X2 = SUMX(FILTER(ADDXATABLE(X_Column,Y_Column),ISNUMBER([X])&&ISNUMBER([Y])), [X]*[X])
VAR Corr_Coef_Y2 = SUMX(FILTER(ADDXATABLE(X_Column,Y_Column),ISNUMBER([X])&&ISNUMBER([Y])), [Y]*[Y])

RETURN
DIVIDE(
    COUNTROWS(X_Column) * Corr_Coef_XY - Corr_Coef_X * Corr_Coef_Y,
    SQRT((COUNTROWS(X_Column) * Corr_Coef_X2 - Corr_Coef_X^2) * (COUNTROWS(X_Column) * Corr_Coef_Y2 - Corr_Coef_Y^2)),
    0
)
