from datetime import datetime

records_list = []


class Incidences():
    """This class contains incidents model methods"""
    def __init__(self):
        self.incident = records_list

    def save(self, created_by, record_type, location, comment):
        """"Method to save red-flags"""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

        return data

    def get_all_records(self):
        """retrieves all the records"""

        return self.incident

    def get_one_record(self, record_id):
        """retrieves one record"""

        record = [record for record in records_list if record["record_id"] == record_id]
        return record

    def update_record(self, comment, index):
        """Edit existing record comment"""

        data = comment

        for comment in records_list:
            records_list[index]['comment'] = data
            

    def update_record_location(self, location, index):
        """Edit existing record location"""

        data = location

        for location in records_list:
            records_list[index]['location'] = data

    def get_index(self, records_id):
        """Get index position of a record"""

        index = 0
        for record in records_list:
            if record["record_id"] == records_id:
                return index
            index += 1

        return index

