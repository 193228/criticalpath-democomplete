def queryAperturaMaterias(listaPeriodo,clave):
    consulta = f'''
                select mat.materiaid, mat.Nombre, mat.Periodo from d_materia mat
                left join d_planestudios plan on mat.PlanEstudiosID = plan.PlanEstudiosID
                where mat.Periodo in {str(tuple(listaPeriodo))} and plan.clave = {clave}
                '''
    return consulta

def queryDatosAlumno(matricula):
    consulta = f'''
                SELECT cal.Matricula, mat.Nombre, cal.materiaid, cal.fechaperiodoid, mat.periodo, cal.Final, cal.Aprobado FROM d_calificaciones cal 
                LEFT JOIN d_materia mat ON mat.MateriaID = cal.MateriaID 
                LEFT JOIN d_planestudios plan ON plan.PlanEstudiosID = mat.PlanEstudiosID 
                LEFT JOIN c_estatuscardex e ON e.EstatusCardexID = cal.EstatusCardexID 
                WHERE cal.Matricula = {matricula}
                '''
    return consulta