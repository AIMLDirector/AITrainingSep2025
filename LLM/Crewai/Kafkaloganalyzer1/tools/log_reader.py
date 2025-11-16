from crewai.tools import tool

@tool
def read_log_file():
    """Reads kafka.log from the current directory"""
    try:
        with open("kafka.log", "r") as file:
            return file.read()
    except Exception as e:
        return f"Error reading log: {e}"

