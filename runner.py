from scripts.final.get_hta_records import get_hta_records

if __name__ == "__main__":
    hta_records = get_hta_records()
    print(len(hta_records.records), " records found")

    print(hta_records.records[0])