class Entry:
    m_name = ""
    m_description = "Please fill the description."
    m_required = "No"
    m_default = "-"
    m_value = "-"
    m_example = "Please fill the example."

    def __init__(self, name, required, default):
        self.m_name = name
        self.m_required = required
        self.m_default = default