from handlers.file_handler import write_data_to_file, write_forms_to_file


class Writer:
    def __init__(self, all_lists):
        self.all_lists = all_lists

    def write_target_success(self):
        file_names = {
            "target_forms_COMMAND": "forms_COMMAND_success",
            "target_forms_not_vulnerable": "forms_not_vulnerable",
        }

        for list_name, file_name in file_names.items():
            if self.all_lists[list_name]:
                if "forms" in list_name and list_name != "target_forms_not_vulnerable":
                    print(write_forms_to_file(self.all_lists[list_name], file_name))
                else:
                    print(write_data_to_file(self.all_lists[list_name], file_name))
