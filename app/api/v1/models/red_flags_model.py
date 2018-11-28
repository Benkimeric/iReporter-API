from datetime import datetime

records_list = []


class Incidences():
    def __init__(self):
        self.incident = records_list


    def save(self, created_by, record_type, location, comment):
        """"Method to save red-flags,def"""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:S")
        status = "Draft"
        data = {
            "record_id": len(self.incident)+1,
            "createdOn": date,
            "created_by": created_by,
            "record_type": record_type,
            "location": location,
            "status": status,
            "comment": comment
        }

        self.incident.append(data)

        return self.incident