Corr_Coef = 
VAR CurrentX = SELECTEDVALUE(Kpi_list[Value])
VAR CurrentY = SELECTEDVALUE(Kpi_list_2[Value])
VAR V_table  = SUMMARIZE(
        kpi_sumarized,
        kpi_sumarized[Date],
        "x", SWITCH(TRUE(),  CurrentX = "BBAS3" ,  MAX(kpi_sumarized[BBAS3]),
                             CurrentX = "BBDC4" ,  MAX(kpi_sumarized[BBDC4]),
                             CurrentX = "BPAC11",  MAX(kpi_sumarized[BPAC11]),
                             CurrentX = "INBR32",  MAX(kpi_sumarized[INBR32]),
                             CurrentX = "ITUB3" ,  MAX(kpi_sumarized[ITUB3]),
                             CurrentX = "ROXO34",  MAX(kpi_sumarized[ROXO34]),
                             CurrentX = "SANB11",  MAX(kpi_sumarized[SANB11])),

        "y", SWITCH(TRUE(),  CurrentY = "BBAS3" , MAX(kpi_sumarized[BBAS3]),
                             CurrentY = "BBDC4" , MAX(kpi_sumarized[BBDC4]),
                             CurrentY = "BPAC11", MAX(kpi_sumarized[BPAC11]),
                             CurrentY = "INBR32", MAX(kpi_sumarized[INBR32]),
                             CurrentY = "ITUB3" , MAX(kpi_sumarized[ITUB3]),
                             CurrentY = "ROXO34", MAX(kpi_sumarized[ROXO34]),
                             CurrentY = "SANB11", MAX(kpi_sumarized[SANB11]))
                        )
VAR n = DISTINCTCOUNT(kpi_sumarized[Date])
                                               
RETURN 
VAR Corr_coef_X = SUMX(V_table, [x])
VAR Corr_coef_Y = SUMX(V_table, [y])
VAR Corr_coef_XY = SUMX(V_table, [x]*[y])
VAR Corr_coef_X2 = SUMX(V_table, [x]*[x])
VAR Corr_coef_Y2 = SUMX(V_table, [y]*[y])


RETURN
DIVIDE((n*[Corr_coef_XY]-[Corr_coef_X]*[Corr_coef_Y]),
    SQRT((n*[Corr_coef_X2]-[Corr_coef_X]^2)*(n*[Corr_coef_Y2]-[Corr_coef_Y]^2)),0)
