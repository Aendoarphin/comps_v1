from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QFileDialog
from io import BytesIO
from PIL import Image
from gui.dialog import show_dialog
import re, requests, json, csv, os

# Checks format of user search term
# Sorts collection of products based on sale price
# Reformats stringified response data
# Converts product image to a compatible data type
# Converts files, json, csv, txt
# Prompts user for save location
# Checks for valid path

class Utils:

    # Accept only alphanumerics and chars #, /, (, ), -
    def validate_input(self, input_str):
        if re.match("^[a-zA-Z0-9 #/\-\(\).]+$", input_str):
            return True
        else:
            return False

    # Sort the data to show the highest or lowest item first
    def sort_data(self, data: dict, order: str):
        products = data.get("products")
        reverse_order = True if order == "desc" else False
        sorted_items = sorted(products, key=lambda x: x["sale_price"], reverse=reverse_order)
        return sorted_items

    # Return data of response in formatted string
    def get_data(self, data, sort_order):
        br = "<br>"
        space = br*2
        # Get the list of products from the data dictionary
        searched_items = data.get("products")
        output = ""

        # Check if there are any products in the list
        if searched_items:
            # Extract the relevant data from the data dictionary
            total_results = data.get("total_results", 0)
            average_price = data.get("average_price", 0)
            min_price = data.get("min_price", 0)
            max_price = data.get("max_price", 0)

            # Append a summary of the search results to the output string
            output += (f"<b><u>SEARCH RESULTS SUMMARY</u></b> {space}"
                    f"Total Results: {total_results:<.0f}{br}"
                    f"Average Price: ${average_price:<.2f}{br}"
                    f"Minimum Price: ${min_price:<.2f}{br}"
                    f"Maximum Price: ${max_price:<.2f}{space}")

            # Sort the list of products based on their sale price
            sorted_items = self.sort_data(data, sort_order)

            # Iterate through the sorted list of products
            for i, product in enumerate(sorted_items, 1):
                output += f"<u><b>Item {i} {space}</b></u>"
                # Iterate through the key-value pairs in the current product dictionary
                for key, value in product.items():
                    # Check each key and append the corresponding value to the output string
                    if key == "title":
                        output += f"<u>Title</u>: {value} {br}"
                    elif key == "condition":
                        output += f"<u>Condition</u>: {value} {br}"
                    elif key == "buying_format":
                        output += f"<u>Buying Format</u>: {value} {br}"
                    elif key == "sale_price":
                        output += f"<u>Sale Price</u>: {value} {br}"
                    elif key == "date_sold":
                        output += f"<u>Date Sold</u>: {value} {br}"
                    elif key == "image_url":
                        output += f'<u>Image</u>: <a style ="color: purple;" href="{value}" target="_blank">Go to image</a> {br}'
                    elif key == "shipping_price":
                        output += f"<u>Shipping Price</u>: {value}{br}"
                    elif key == "link":
                        output += f'<u>Link</u>: <a style ="color: purple;" href="{value}" target="_blank">Go to listing</a> {br}'
                output += space
            return output
        else:
            output = "No results found."

    # Convert WEBP -> PNG -> QPixmap
    def webp_to_pixmap(self, link: str) -> QPixmap:
        response = requests.get(link)
        im_bytes = BytesIO(response.content)
        im = Image.open(im_bytes)

        img = BytesIO()
        im.convert("RGB").save(img, "PNG")
        img.seek(0)
        data = img.getvalue()
        
        img_data = QImage()
        img_data.loadFromData(data, format="Format_ARGB32")
        pixmap = QPixmap.fromImage(img_data)
        return pixmap

    # Get image from the highest or lowest sold item, then convert to QPixmap
    def get_pixmap(self, data: dict, order: str) -> QPixmap:
        if data:
            products = data.get("products")
            if products:
                sorted_items = sorted(
                    products, 
                    key=lambda x: x["sale_price"], 
                    reverse=(order == "desc"))
                if sorted_items:
                    first_item = sorted_items[0]["image_url"]
                    card_image = self.webp_to_pixmap(first_item)
                    return card_image
        return None
    
    # Dictionary to {filetype} conversions
    def dict_to_txt(self, data: dict, filepath: str, filename: str = None):
        if filename is None:
            file_path = filepath
        else:
            filename = filename.replace('/', '_')
            file_path = f"{filepath}\\{filename}.txt"


        with open(file_path, 'w', encoding='utf-8') as f:
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                    # Handle list of dicts
                    f.write(f"{key}:\n")
                    for i, d in enumerate(value):
                        f.write(f"  - Item {i + 1}:\n")
                        for k, v in d.items():
                            f.write(f"    {k}: {v}\n")
                else:
                    # Handle other values
                    f.write(f"{key}: {value}\n")

    def dict_to_json(self, data: dict, filepath: str):
        with open(f"{filepath}", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    def dict_to_csv(self, data: dict, filepath: str):
        products = data.get('products')
        if not products:
            show_dialog("error", "No products found")
            return

        with open(f"{filepath}", 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(products[0].keys())  # write the columns headers
            for product in products:
                writer.writerow(product.values())  # write each product values as a row

    # Display dialog for saving file
    def save_as_dialog(self, data: dict):
        file_types = "JSON (*.json);;Text (*.txt);;CSV (*.csv)"
        file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", file_types)

        if file_path:
            if file_path.endswith('.json'):
                self.dict_to_json(data, file_path)
                show_dialog("success", f"File was saved:\n{file_path}")
            elif file_path.endswith('.txt'):
                self.dict_to_txt(data, file_path)
                show_dialog("success", f"File was saved:\n{file_path}")
            elif file_path.endswith('.csv'):
                self.dict_to_csv(data, file_path)
                show_dialog("success", f"File was saved:\n{file_path}")
            else:
                print("Unsupported file type.")

    # Return string path
    def choose_path(self):
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
        if folder_path != "":
            self.validate_path(folder_path)
            return folder_path
        else:
            return ""
    
    def validate_path(self, path: str):
        folder_path = path
        # If the path is an existing directory
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            return folder_path
        else:
            return "invalid"