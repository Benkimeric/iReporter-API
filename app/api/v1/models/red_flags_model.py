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

        #return the whole list
        # return self.incident
        #return new data
        return data

    def get_all_records(self):
        """get all the records"""

        return records_list

    def get_one_record(self, record_id):
        """get one record"""

        record = [record for record in records_list if record["record_id"] == record_id]
        return record

    def update_record(self, comment, index):
        """Edit existing record"""

        data = comment

        for comment in records_list:
            records_list[index]['comment'] = data
            # return records_list

    def get_index(self, records_id):
        """Get index position of a record"""

        index = 0
        for record in records_list:
            if record["record_id"] == records_id:
                return index
            index += 1

        return index