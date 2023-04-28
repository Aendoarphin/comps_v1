from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication
import matplotlib.pyplot as plt, io, base64, datetime

# Generates a sorted chart

class Chart:
    def generate_chart(self, response, text_color) -> QPixmap | None:
        # Check if there is a response before generating the chart
        if response:
            # Sort the products by date sold
            products = self.sort_by_date_sold(response)
            # Get the dates and sale prices
            dates = [product['date_sold'] for product in products]
            prices = [product['sale_price'] for product in products]

            # Create a new figure and axis
            fig, ax = plt.subplots(facecolor='none')
            # Plot the line chart
            ax.plot(dates, prices, color='#3f4753', linewidth=1)
            # Set the x and y labels and title
            ax.set_xlabel('Date Sold', color=text_color)
            ax.set_ylabel('Sale Price', color=text_color)
            ax.set_title('Price vs. Date', color=text_color)

            # Set the x-ticks and x-tick labels
            num_products = len(dates)
            if num_products % 2 == 0:
                # If the number of products is even, set 3 x-tick labels
                middle = num_products // 2
                x_labels = [dates[0], dates[middle], dates[-1]]
            else:
                # If the number of products is odd, set 4 x-tick labels
                middle_left = num_products // 2 - 1
                x_labels = [dates[0], dates[middle_left], dates[num_products // 2], dates[-1]]
            ax.set_xticks(x_labels)
            ax.set_xticklabels(x_labels, fontsize=8, rotation=0, color=text_color)

            # Set the color of the x and y axes and ticks
            ax.spines['bottom'].set_color(text_color)
            ax.spines['left'].set_color(text_color)
            ax.tick_params(axis='x', colors=text_color)
            ax.tick_params(axis='y', colors=text_color)

            # Save the chart as a PNG, store image in memory buffer as bytes,
            # and convert the image data to a string
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            img_data = base64.b64encode(img.getvalue()).decode('utf-8')

            # Create the pixmap
            app = QApplication.instance()
            pixmap = QPixmap()
            pixmap.loadFromData(base64.b64decode(img_data))

            # Return the pixmap
            return pixmap
        else:
            # If there is no response, return None
            return None

    def sort_by_date_sold(self, response) -> list[dict]:
        products = response['products']
        
        # Convert the date strings to datetime objects
        for product in products:
            date_string = product['date_sold']
            try:
                product['date_sold'] = datetime.datetime.strptime(date_string, '%B %d, %Y')
            except ValueError:
                # Try another format
                product['date_sold'] = datetime.datetime.strptime(date_string, '%b %d, %Y')
        
        # Sort the products by date sold
        products.sort(key=lambda x: x['date_sold'], reverse=False)
        
        # Reformat the dates for display
        for product in products:
            product['date_sold'] = product['date_sold'].strftime('%B %d, %Y')
        
        return products

