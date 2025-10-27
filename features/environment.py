from selenium import webdriver

def before_scenario(context, scenario):
    """
    Esta función se ejecuta antes de cada escenario de prueba.
    Inicializa el WebDriver y lo almacena en el contexto.
    """
    # placeholder por si se necesita setup global
    pass

def after_scenario(context, scenario):
    """
    Esta función se ejecuta después de cada escenario de prueba.
    Cierra el navegador para limpiar después de cada prueba.
    """
    # Asegurar cierre del navegador siempre
    if hasattr(context, "driver") and getattr(context, "driver") is not None:
        try:
            context.driver.quit()
        except Exception:
            pass
