import base64

def mask_pii(data):
    """
    Masks data fields such as device_id and ip using base64 encoding. base64 encoding is reversible.
    """
    masked_data = data.copy()
    
    masked_data['masked_device_id'] = base64.b64encode(data['device_id'].encode()).decode()
    masked_data['masked_ip'] = base64.b64encode(data['ip'].encode()).decode()

    app_version_new = int(''.join(masked_data['app_version'].split(".")))  
    masked_data['app_version'] = app_version_new

    return masked_data
