Feature: Buscar un artista y validar la fecha del ultimo release
    Scenario: Validar la fecha del ultimo lanzamiento de Bruno Mars
        Given el usuario está en el home page de last.fm
        when busca al artista "Bruno Mars"
        and selecciona el primer resultado
        then la fecha del ultimo release debe ser "3 octubre 2025"