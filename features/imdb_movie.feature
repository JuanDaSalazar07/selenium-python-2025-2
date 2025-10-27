Feature: Buscar una película en IMDb y validar su calificación
  Scenario: Buscar la película "Inception" y verificar su calificación
    Given el usuario está en la página de inicio de IMDb
    When busca la película "Inception" en IMDb
    And selecciona el primer resultado de IMDb
    Then el título de la película debe ser "El origen" en IMDb
    And la calificación debe ser "8,8" en IMDb 