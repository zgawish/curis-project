

process setup {
    """
    python3 setup.py
    """
}

process startServer {
    """
    python3 ./../communication/serverclass.py &
    """
}
