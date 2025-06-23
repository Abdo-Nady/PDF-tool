import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
import os

class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Tool")
        self.root.geometry("600x550")
        self.root.configure(bg="#f5f5f5")

        self.current_frame = None
        self.button_style = {"font": ("Helvetica", 12), "bg": "#4CAF50", "fg": "white", "bd": 0, "padx": 10, "pady": 5}
        self.show_main_menu()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_main_menu(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.current_frame.pack(fill="both", expand=True)

        tk.Label(self.current_frame, text="PDF Tool", font=("Arial", 20, "bold"), bg="#f5f5f5").pack(pady=20)
        tk.Label(self.current_frame, text="What do you want to do?", font=("Arial", 14), bg="#f5f5f5").pack(pady=10)

        tk.Button(self.current_frame, text="📎 Merge PDFs", command=self.show_merge_window, width=50, height=3, **self.button_style).pack(pady=10)
        tk.Button(self.current_frame, text="✂️ Split PDF", command=self.show_split_window, width=50,height=3, **self.button_style).pack(pady=10)

    def show_merge_window(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.current_frame.pack(fill="both", expand=True)

        self.pdf_files = []

        tk.Button(self.current_frame, text="← Back", command=self.show_main_menu, **self.button_style).pack(anchor="w", padx=10, pady=10)
        tk.Label(self.current_frame, text="Selected PDFs:", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(pady=5)

        self.file_frame = tk.Frame(self.current_frame, bg="#ffffff", bd=1, relief="sunken")
        self.file_frame.pack(pady=5, padx=20, fill="both", expand=True)

        tk.Button(self.current_frame, text="Add PDFs", command=self.add_pdfs, **self.button_style).pack(pady=5)
        tk.Button(self.current_frame, text="Merge PDFs", command=self.merge_pdfs, **self.button_style).pack(pady=10)

    def refresh_file_list(self):
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        for i, file in enumerate(self.pdf_files):
            row = tk.Frame(self.file_frame, bg="#ffffff")
            row.pack(fill="x", pady=2, padx=5)

            filename = os.path.basename(file)
            tk.Label(row, text=filename, anchor="w", bg="#ffffff").pack(side="left", expand=True, fill="x")
            tk.Button(row, text="⬆️", command=lambda i=i: self.move_up(i), width=3, bg="#e0e0e0").pack(side="right")
            tk.Button(row, text="⬇️", command=lambda i=i: self.move_down(i), width=3, bg="#e0e0e0").pack(side="right")
            tk.Button(row, text="❌", command=lambda i=i: self.remove_file(i), width=3, bg="#ff6666").pack(side="right")

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.pdf_files.extend(files)
            self.refresh_file_list()

    def remove_file(self, index):
        del self.pdf_files[index]
        self.refresh_file_list()

    def move_up(self, index):
        if index > 0:
            self.pdf_files[index], self.pdf_files[index - 1] = self.pdf_files[index - 1], self.pdf_files[index]
            self.refresh_file_list()

    def move_down(self, index):
        if index < len(self.pdf_files) - 1:
            self.pdf_files[index], self.pdf_files[index + 1] = self.pdf_files[index + 1], self.pdf_files[index]
            self.refresh_file_list()

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("Warning", "No PDF files selected.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_path:
            return

        writer = PdfWriter()
        try:
            for file in self.pdf_files:
                reader = PdfReader(file)
                for page in reader.pages:
                    writer.add_page(page)
            with open(output_path, "wb") as f_out:
                writer.write(f_out)
            messagebox.showinfo("Success", f"Merged PDF saved to:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_split_window(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.current_frame.pack(fill="both", expand=True)

        self.pdf_path = ""
        self.page_count = 0

        tk.Button(self.current_frame, text="← Back", command=self.show_main_menu, **self.button_style).pack(anchor="w", padx=10, pady=10)
        tk.Button(self.current_frame, text="Select PDF to Split", command=self.load_pdf, **self.button_style).pack(pady=10)

        self.info_label = tk.Label(self.current_frame, text="", bg="#f5f5f5", font=("Arial", 10))
        self.info_label.pack(pady=5)

        tk.Label(self.current_frame, text="Enter split page numbers (e.g. 3,5,8):", bg="#f5f5f5", font=("Arial", 11)).pack()
        self.entry = tk.Entry(self.current_frame, width=30)
        self.entry.pack(pady=5)

        self.split_button = tk.Button(self.current_frame, text="Split PDF", command=self.split_pdf, state="disabled", **self.button_style)
        self.split_button.pack(pady=20)

    def load_pdf(self):
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file:
            try:
                reader = PdfReader(file)
                self.pdf_path = file
                self.page_count = len(reader.pages)
                self.info_label.config(text=f"✅ Loaded: {os.path.basename(file)}\nPages: {self.page_count}")
                self.split_button.config(state="normal")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load PDF: {str(e)}")

    def split_pdf(self):
        if not self.pdf_path:
            return

        raw_input = self.entry.get().strip()
        if not raw_input:
            messagebox.showwarning("Invalid Input", "Please enter at least one page number.")
            return

        try:
            split_points = sorted(set(int(p.strip()) for p in raw_input.split(",") if p.strip().isdigit()))
            if not split_points or any(p < 1 or p >= self.page_count for p in split_points):
                raise ValueError
        except:
            messagebox.showerror("Invalid Input", "Please enter valid page numbers (1 to N-1).")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file:
            return

        base_name = os.path.splitext(os.path.basename(output_file))[0]
        save_dir = os.path.join(os.path.dirname(output_file), base_name + "_split")
        os.makedirs(save_dir, exist_ok=True)

        try:
            reader = PdfReader(self.pdf_path)
            all_pages = list(range(self.page_count))
            split_ranges = []

            prev = 0
            for point in split_points:
                split_ranges.append(all_pages[prev:point])
                prev = point
            split_ranges.append(all_pages[prev:])

            for i, pages in enumerate(split_ranges):
                writer = PdfWriter()
                for page_num in pages:
                    writer.add_page(reader.pages[page_num])
                output_path = os.path.join(save_dir, f"part_{i + 1}.pdf")
                with open(output_path, "wb") as f_out:
                    writer.write(f_out)

            messagebox.showinfo("Success", f"PDF split into {len(split_ranges)} parts.\nSaved in folder:\n{save_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"Split failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToolApp(root)
    root.mainloop()