import phonenumbers
from phonenumbers import geocoder, timezone
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk  # Import ttk for combobox
import requests
from dotenv import load_dotenv
import os
load_dotenv() 
class PhoneNumberInfoApp:
    """Phone Number Information Finder Application"""

    def __init__(self, root):
        self.root = root
        self.root.title("Phone Number Info Finder")

        # Set window size to fill the entire screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")  # Full screen size
        self.root.resizable(True, True)  # Allow resizing

        # Set colors
        self.bg_color = "#F0F8FF"  # Light blue background
        self.text_color = "#2F4F4F"  # Dark Slate Gray text
        self.button_color = "#E0E0E0"  # Light grey button background
        self.button_text_color = "#000000"  # Black text for buttons
        self.result_text_color = "#333333"  # Dark text for result

        self.result_label = None  # Placeholder for result label
        self.screen_width = screen_width  # Storing screen width for later use
        self.setup_ui()

    def setup_ui(self):
        """Set up the GUI elements with adjusted sizes and improved layout."""
        self.root.configure(bg=self.bg_color)

        # Title Label
        title_label = tk.Label(
            self.root,
            text="Phone Number Information Finder",
            font=("Arial", 18, 'bold'),
            fg=self.text_color,
            bg=self.bg_color
        )
        title_label.pack(pady=40)

        # Phone Number Input Label and Country Code Selection
        label = tk.Label(
            self.root,
            text="Select Country Code and Enter Phone number:",
            font=("Arial", 14),
            fg=self.text_color,
            bg=self.bg_color
        )
        label.pack(pady=10)

        # Create a combobox for selecting the country code
        self.country_code_combobox = ttk.Combobox(
            self.root, 
            font=("Arial", 16), 
            width=10,
            state="readonly"
        )
        
        # Dynamically get all country codes
        country_codes = self.get_all_country_codes()
        
        # Populate combobox with country codes
        self.country_code_combobox['values'] = country_codes
        self.country_code_combobox.set("+1")  # Set default country code as +1
        self.country_code_combobox.pack(pady=10)

        # Phone Number Entry Field
        self.entry = tk.Entry(self.root, font=("Arial", 16), width=40, bd=2, relief="solid")
        self.entry.pack(pady=20)

        # Button Frame with 3 buttons: Get Info, Clear, Save
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)

        self.create_button(button_frame, "Get Info", self.get_phone_info)
        self.create_button(button_frame, "Clear", self.clear_input)
        self.create_button(button_frame, "Save Result", self.save_result)

        # Result Label with increased height
        self.result_label = tk.Text(
            self.root,
            font=("Arial", 16),
            fg=self.result_text_color,
            bg=self.bg_color,
            wrap="word",  # Wrap text to prevent overflow
            width=50,
            height=6,
            relief="solid",  # Border around the result area
            bd=2
        )
        self.result_label.pack(pady=30)

        # Insert the placeholder text when the app starts
        self.result_label.insert(tk.END, "Result will be shown here...")
        self.result_label.config(state=tk.DISABLED)  # Make it read-only initially

    def create_button(self, frame, text, command):
        """Create and style a compact button."""
        button = tk.Button(
            frame,
            text=text,
            font=("Arial", 12),
            bg=self.button_color,
            fg=self.button_text_color,
            width=12,
            height=2,
            relief="flat",  # Flat design for a modern look
            command=command
        )
        button.pack(side="left", padx=20)

        # Hover effect
        button.bind("<Enter>", lambda e: button.config(bg="#D3D3D3"))  # Light grey hover
        button.bind("<Leave>", lambda e: button.config(bg=self.button_color))  # Revert to original

    def get_all_country_codes(self):
        """Fetch all country codes dynamically from phonenumbers."""
        country_codes = []
        for country_code, region_codes in phonenumbers.COUNTRY_CODE_TO_REGION_CODE.items():
            country_codes.append(f"+{country_code}")
        return sorted(country_codes)

    def get_phone_info(self):
        """Fetch and display phone number information."""
        country_code = self.country_code_combobox.get()  # Get selected country code
        mobile_no = self.entry.get()
        
        # Combine country code with phone number
        full_number = country_code + mobile_no
        
        try:
            mobile_no_parsed = phonenumbers.parse(full_number)
            if phonenumbers.is_valid_number(mobile_no_parsed):
                # Get the basic information
                region = ', '.join(timezone.time_zones_for_number(mobile_no_parsed))
                country = geocoder.description_for_number(mobile_no_parsed, 'en')

                # Get the current service provider
                current_service_provider = self.get_current_service_provider(mobile_no_parsed)

                # Format the result in one line for each question and answer
                result_text = (
                    f"Phone Number belongs to region: {region}\n"
                    f"Service Provider: {current_service_provider}\n"
                    f"Phone number belongs to country: {country}"
                )

                # Display the result inside the Text widget
                self.result_label.config(state=tk.NORMAL)  # Make the widget editable
                self.result_label.delete(1.0, tk.END)  # Clear any previous content
                self.result_label.insert(tk.END, result_text)  # Insert the result text
                self.result_label.config(state=tk.DISABLED)  # Make it read-only again

            else:
                self.result_label.config(state=tk.NORMAL)  # Make it editable
                self.result_label.delete(1.0, tk.END)
                self.result_label.insert(tk.END, "Invalid phone number. Please try again.")
                self.result_label.config(state=tk.DISABLED)

        except phonenumbers.phonenumberutil.NumberParseException:
            self.result_label.config(state=tk.NORMAL)  # Make it editable
            self.result_label.delete(1.0, tk.END)
            self.result_label.insert(tk.END, "Invalid input format. Please include the country code (e.g., +1 xxxxxxxxx).")
            self.result_label.config(state=tk.DISABLED)

    def clear_input(self):
        """Clear the input and result fields.""" 
        self.entry.delete(0, tk.END)
        self.result_label.config(state=tk.NORMAL)  # Make the widget editable
        self.result_label.delete(1.0, tk.END)  # Clear the result
        self.result_label.insert(tk.END, "Result will be shown here...")  # Reset to placeholder
        self.result_label.config(state=tk.DISABLED)  # Make it read-only again

    def save_result(self):
        """Save the result to a file."""
        result = self.result_label.get(1.0, tk.END).strip()  # Get text from Text widget
        if not result or result == "Result will be shown here...":
            messagebox.showwarning("No Result", "No information to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", ".txt"), ("All Files", ".*")],
            title="Save Result"
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(result)
            messagebox.showinfo("Success", "Result saved successfully!")

    def get_current_service_provider(self, mobile_no_parsed):
        """Get the current service provider of the phone number using the NumVerify API."""
        api_key = os.getenv("NUMVERIFY_API_KEY")  # Replace with your NumVerify API key
        formatted_number = phonenumbers.format_number(mobile_no_parsed, phonenumbers.PhoneNumberFormat.E164)
        url = f"http://apilayer.net/api/validate?access_key={api_key}&number={formatted_number}"

        try:
            response = requests.get(url)
            data = response.json()

            if data.get('valid'):
                # Get the carrier information from the API response
                service_provider = data.get('carrier', 'Carrier info not available')
                return service_provider
            else:
                return "Carrier info not available"
        except requests.exceptions.RequestException as e:
            print("Error fetching data:", e)
            return "API request failed"


root = tk.Tk()
app = PhoneNumberInfoApp(root)
root.mainloop()
