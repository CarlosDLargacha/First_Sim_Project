import logging

def get_logger(name):
    """Configura y devuelve un logger listo para usar"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Formato del log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Solo añadir handlers si no existen ya
    if not logger.handlers:
        # Handler para consola
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # Handler para archivo
        fh = logging.FileHandler('simulation.log', mode='w')  # Sobreescribe el archivo cada ejecución
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger