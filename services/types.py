"""
Descriptive service type codes, for code readability.
"""

# Online consultation between a doctor and a patient
CONSULTATION = 'C'

# Convert from service code to verbose name
# e.g. 'C' => "在线咨询"
SERVICE_NAME = {
    CONSULTATION: "在线咨询",
}

# Get description of service
SERVICE_DESCRIPTION = {
    CONSULTATION: "医生向患者提供在线咨询、答疑和诊断服务",
}
