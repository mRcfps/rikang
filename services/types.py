"""
Descriptive service type codes, for code readability.
"""

# Online consultation between a doctor and a patient
CONSULTATION = 'C'

# Annual membership
MEMBERSHIP = 'M'

# Convert from service code to verbose name
# e.g. 'C' => "在线咨询"
service_name = {
    CONSULTATION: "在线咨询",
    MEMBERSHIP: "会员",
}

# Get description of service
service_description = {
    CONSULTATION: "医生向患者提供在线咨询、答疑和诊断服务",
    MEMBERSHIP: "日康平台年费会员",
}

from_service_name = {
    "在线咨询": CONSULTATION,
    "会员": MEMBERSHIP,
}