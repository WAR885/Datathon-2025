"""
dashboard.py

Tkinter dashboard that:
- Embeds a matplotlib profits figure on the "Overall" tab
- Shows top-3 menu items & ingredients overall
- Allows selecting a month to view top-3 menu items & ingredients for that month
- Shows predicted profit and predicted top items/ingredients on "Future prediction" tab

How to connect your processed data:
- If you already have a matplotlib Figure object for profits, assign it to `profits_fig`
  (set USE_PROFITS_FIG=True and assign profits_fig).
- Alternatively, save your figure as an image (png) and set PROFITS_IMAGE_PATH to point to it.
- Or provide the data structures described below and let the script create the figure.

Expected data structures (examples shown in the demo below):
- overall_top_items: list of (name, count) sorted descending (top 3 used)
- overall_top_ingredients: list of (name, amount)
- monthly_top_items: dict of month_str -> list of (name,count)
- monthly_top_ingredients: dict of month_str -> list of (name,amount)
- predicted_profit: float
- predicted_top_items, predicted_top_ingredients: lists of (name,predicted_count/amount)

"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import csv
import io
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
import random
from datetime import datetime
from overall_insights import *

# ---------------------------
# USER CONFIG / PLACE YOUR DATA HERE
# ---------------------------

# Option A: If you have a matplotlib Figure object already, set this to True and assign `profits_fig`.

data_insights = overall_insights()

USE_PROFITS_FIG = False
profits_fig = None  # replace with your matplotlib.figure.Figure if you have one

# Option B: If you have a saved profit image, set this path (png/jpg)
PROFITS_IMAGE_PATH = "total_earnings.png"  # e.g. "profits.png"

profits_data = data_insights.yearly_earnings

# Example processed lists (replace with your actual processed results)
overall_top_items = sorted(((k, int(v)) for k, v in data_insights.total_pop_items.items()), key=lambda kv: kv[1], reverse=True)
overall_top_ingredients = sorted(((k, int(v)) for k, v in data_insights.total_pop_ingredients.items()), key=lambda kv: kv[1], reverse=True)

monthly_top_items = data_insights.item_pops


monthly_top_ingredients = data_insights.ingredient_pops

predicted_profit = data_insights.projected_earnings
predicted_top_items = items = sorted(((k, int(v)) for k, v in data_insights.projected_pop_items.items()), key=lambda kv: kv[1], reverse=True)
predicted_top_ingredients = sorted(((k, int(v)) for k, v in data_insights.projected_pop_ingredients.items()), key=lambda kv: kv[1], reverse=True)

# ---------------------------
# End of user-editable data
# ---------------------------

# Utility: create a matplotlib Figure if needed
def create_profits_figure_from_list(profits_list):
    months = [m for m, v in profits_list]
    vals = [v for m, v in profits_list]
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
    ax.plot(months, vals, marker='o', linewidth=2)
    ax.set_title("Monthly Profits")
    ax.set_ylabel("Profit ($)")
    ax.grid(True, linestyle='--', alpha=0.4)
    # annotate last value
    ax.annotate(f"{vals[-1]:.2f}", xy=(len(vals)-1, vals[-1]), xytext=(0,8),
                textcoords="offset points", ha='center')
    plt.tight_layout()
    return fig

# Prepare profits figure depending on available input
def get_profits_figure():
    if USE_PROFITS_FIG and profits_fig is not None:
        return profits_fig
    if PROFITS_IMAGE_PATH:
        # load the image into a matplotlib figure
        try:
            import matplotlib.image as mpimg
            arr = mpimg.imread(PROFITS_IMAGE_PATH)
            fig, ax = plt.subplots(figsize=(6,3.5), dpi=100)
            ax.axis('off')
            ax.imshow(arr)
            plt.tight_layout()
            return fig
        except Exception as e:
            print("Failed to load profits image:", e)

# GUI app
class DashboardApp(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        root.title("Inventory Intelligence Dashboard")
        root.geometry("1000x650")
        self.style = ttk.Style(root)
        # Basic theme tuning
        try:
            self.style.theme_use('clam')
        except:
            pass

        # Notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=6, pady=6)

        # Create tabs
        self.tab_overall = ttk.Frame(self.notebook)
        self.tab_month = ttk.Frame(self.notebook)
        self.tab_future = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_overall, text="Overall")
        self.notebook.add(self.tab_month, text="Month-by-month")
        self.notebook.add(self.tab_future, text="Future prediction")

        self.setup_overall_tab()
        self.setup_month_tab()
        self.setup_future_tab()

        self.pack(fill='both', expand=True)

    # ---------------
    # OVERALL
    # ---------------
    def setup_overall_tab(self):
        left = ttk.Frame(self.tab_overall)
        right = ttk.Frame(self.tab_overall, width=280)
        left.pack(side='left', fill='both', expand=True, padx=(8,4), pady=8)
        right.pack(side='right', fill='y', padx=(4,8), pady=8)

        # Matplotlib figure embed
        fig = get_profits_figure()
        self.canvas = FigureCanvasTkAgg(fig, master=left)
        self.canvas.draw()
        widget = self.canvas.get_tk_widget()
        widget.pack(fill='both', expand=True)

        # Right-side: top 3 items and ingredients overall
        lbl_items = ttk.Label(right, text="Top 3 Menu Items (Overall)", font=("Segoe UI", 11, "bold"))
        lbl_items.pack(anchor='n', pady=(6,2))
        self.items_tree = ttk.Treeview(right, columns=("name","count"), show="headings", height=4)
        self.items_tree.heading("name", text="Item")
        self.items_tree.heading("count", text="Count")
        self.items_tree.column("name", width=160, anchor='w')
        self.items_tree.column("count", width=80, anchor='center')
        self.items_tree.pack(pady=(0,8))

        lbl_ing = ttk.Label(right, text="Top 3 Ingredients (Overall)", font=("Segoe UI", 11, "bold"))
        lbl_ing.pack(anchor='n', pady=(6,2))
        self.ing_tree = ttk.Treeview(right, columns=("name","amt"), show="headings", height=4)
        self.ing_tree.heading("name", text="Ingredient")
        self.ing_tree.heading("amt", text="Amount")
        self.ing_tree.column("name", width=160, anchor='w')
        self.ing_tree.column("amt", width=80, anchor='center')
        self.ing_tree.pack(pady=(0,8))

        self.refresh_overall()

    def refresh_overall(self):
        # populate top items
        for r in self.items_tree.get_children():
            self.items_tree.delete(r)
        for name, cnt in (overall_top_items[:3] if overall_top_items else []):
            self.items_tree.insert("", "end", values=(name, cnt))

        # populate top ingredients
        for r in self.ing_tree.get_children():
            self.ing_tree.delete(r)
        for name, amt in (overall_top_ingredients[:3] if overall_top_ingredients else []):
            self.ing_tree.insert("", "end", values=(name, amt))

        # if profits fig is dynamic, re-embed
        try:
            fig = get_profits_figure()
            self.canvas.figure = fig
            self.canvas.draw()
        except Exception as e:
            print("Could not refresh figure:", e)

    # ---------------
    # MONTH-BY-MONTH
    # ---------------
    def setup_month_tab(self):
        top = ttk.Frame(self.tab_month)
        bot = ttk.Frame(self.tab_month)
        top.pack(fill='x', padx=8, pady=(8,4))
        bot.pack(fill='both', expand=True, padx=8, pady=(4,8))

        ttk.Label(top, text="Select month:", font=("Segoe UI", 10)).pack(side='left', padx=(0,8))
        month_list = ["May","June","July","August","September","October"]

        self.month_cb = ttk.Combobox(top, values=month_list, state="readonly")
        self.month_cb.pack(side='left')
        if month_list:
            self.month_cb.set(month_list[0])
        self.month_cb.bind("<<ComboboxSelected>>", lambda e: self.populate_month_view())


        self.month_fig, self.month_ax = plt.subplots(figsize=(5,3), dpi=100)
        self.month_canvas = FigureCanvasTkAgg(self.month_fig, master=bot)
        self.month_canvas.get_tk_widget().pack(fill='both', expand=True, pady=(2,2))
        # Two Treeviews side-by-side for items & ingredients
        left = ttk.Frame(bot)
        right = ttk.Frame(bot)
        left.pack(side='left', fill='both', expand=True, padx=(0,4))
        right.pack(side='right', fill='both', expand=True, padx=(4,0))

        ttk.Label(left, text="Top Menu Items (This month)", font=("Segoe UI", 11, "bold")).pack(anchor='nw')
        self.month_items = ttk.Treeview(left, columns=("item","count"), show="headings")
        self.month_items.heading("item", text="Item")
        self.month_items.heading("count", text="Count")
        self.month_items.column("item", width=260, anchor='w')
        self.month_items.column("count", width=80, anchor='center')
        self.month_items.pack(fill='both', expand=True, pady=(4,8))

        ttk.Label(right, text="Top Ingredients (This month)", font=("Segoe UI", 11, "bold")).pack(anchor='nw')
        self.month_ings = ttk.Treeview(right, columns=("ing","amt"), show="headings")
        self.month_ings.heading("ing", text="Ingredient")
        self.month_ings.heading("amt", text="Amount")
        self.month_ings.column("ing", width=260, anchor='w')
        self.month_ings.column("amt", width=80, anchor='center')
        self.month_ings.pack(fill='both', expand=True, pady=(4,8))

        # populate initial
        self.populate_month_view()

    def populate_month_view(self):
        m = self.month_cb.get()
        month_names = {"May": 0, "June": 1, "July": 2, "August": 3, "September": 4, "October": 5}

        month_index = month_names[m]
        d = monthly_top_items[month_index]
        items = sorted(((k, int(v)) for k, v in d.items()), key=lambda kv: kv[1], reverse=True)[:7]

        # Clear old plot
        self.month_ax.clear()
        if items:
            names = [x[0] for x in items]
            counts = [x[1] for x in items]
            self.month_ax.bar(names, counts)
            self.month_ax.set_title(f"Top Items in {m}")
            self.month_ax.set_ylabel("Count")
            self.month_ax.set_xticklabels(names, rotation=0, ha='center')

        self.month_canvas.draw()
        # clear
        for r in self.month_items.get_children(): self.month_items.delete(r)
        for r in self.month_ings.get_children(): self.month_ings.delete(r)

        d = monthly_top_items[month_names[m]]
        items = [(k, int(v)) for k, v in sorted(d.items(), key=lambda kv: kv[1], reverse=True)]
        d = monthly_top_ingredients[month_names[m]]
        ings = [(k, int(v)) for k, v in sorted(d.items(), key=lambda kv: kv[1], reverse=True)]

        if not items:
            # fallback: empty placeholders
            items = []
        if not ings:
            ings = []

        for name, cnt in items[:7]:
            self.month_items.insert("", "end", values=(name, cnt))
        for name, amt in ings[:7]:
            self.month_ings.insert("", "end", values=(name, amt))


    # ---------------
    # FUTURE PREDICTION
    # ---------------
    def setup_future_tab(self):
        frame = ttk.Frame(self.tab_future, padding=10)
        frame.pack(fill='both', expand=True)

        top = ttk.Frame(frame)
        top.pack(fill='x')
        ttk.Label(top, text="Predicted Profit (next month):", font=("Segoe UI", 12)).pack(side='left', padx=(0,8))
        self.pred_profit_lbl = ttk.Label(top, text="$0.00", font=("Segoe UI", 14, "bold"))
        self.pred_profit_lbl.pack(side='left')

        # Big card for predicted profit
        card = ttk.Frame(frame, relief='ridge', padding=12)
        card.pack(fill='x', pady=12)

        ttk.Label(card, text="Prediction Summary", font=("Segoe UI", 12, "bold")).pack(anchor='w')
        self.pred_text = tk.Text(card, height=6, wrap='word')
        self.pred_text.pack(fill='x', pady=(8,4))

        # Two lists for predicted items & ingredients
        lists = ttk.Frame(frame)
        lists.pack(fill='both', expand=True)

        left = ttk.Frame(lists)
        right = ttk.Frame(lists)
        left.pack(side='left', fill='both', expand=True, padx=(0,4))
        right.pack(side='right', fill='both', expand=True, padx=(4,0))

        ttk.Label(left, text="Predicted Top Menu Items", font=("Segoe UI", 11, "bold")).pack(anchor='nw')
        self.pred_items_view = ttk.Treeview(left, columns=("item","pred"), show="headings", height = 6)
        self.pred_items_view.heading("item", text="Item")
        self.pred_items_view.heading("pred", text="Predicted")
        self.pred_items_view.column("item", width=260, anchor='w')
        self.pred_items_view.column("pred", width=80, anchor='center')
        self.pred_items_view.pack(fill='x', expand=False, pady=(4,8))

        ttk.Label(right, text="Predicted Top Ingredients", font=("Segoe UI", 11, "bold")).pack(anchor='nw')
        self.pred_ings_view = ttk.Treeview(right, columns=("ing","pred"), show="headings", height=6)
        self.pred_ings_view.heading("ing", text="Ingredient")
        self.pred_ings_view.heading("pred", text="Predicted")
        self.pred_ings_view.column("ing", width=260, anchor='w')
        self.pred_ings_view.column("pred", width=80, anchor='center')
        self.pred_ings_view.pack(fill='x', expand=False, pady=(4,8))

        self.future_fig, self.future_ax = plt.subplots(figsize=(5,3), dpi=100)
        self.future_canvas = FigureCanvasTkAgg(self.future_fig, master=frame)
        self.future_canvas.get_tk_widget().pack(fill='both', expand=True, pady=(4,8))

        btn_export = ttk.Button(frame, text="Export predictions CSV", command=self.export_predictions)
        btn_export.pack(side='bottom', pady=(8,0))

        self.refresh_future()

    def refresh_future(self):
        # predicted profit
        self.pred_profit_lbl.config(text=f"${predicted_profit:,.2f}")

        # populate summary text
        self.pred_text.delete("1.0", "end")
        s = f"Predicted profit for next month: ${predicted_profit:,.2f}\n"
        s += f"Top predicted items: {', '.join([f'{n} ({v})' for n,v in predicted_top_items[:3]])}\n"
        s += f"Top predicted ingredients: {', '.join([f'{n} ({v})' for n,v in predicted_top_ingredients[:3]])}\n"
        s += f"Prediction date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        self.pred_text.insert("1.0", s)

        # fill tables
        for r in self.pred_items_view.get_children(): self.pred_items_view.delete(r)
        for n,v in predicted_top_items[:5]:
            self.pred_items_view.insert("", "end", values=(n, v))

        for r in self.pred_ings_view.get_children(): self.pred_ings_view.delete(r)
        for n,v in predicted_top_ingredients[:5]:
            self.pred_ings_view.insert("", "end", values=(n, v))

        # Draw bar chart for predicted top items
        self.future_ax.clear()
        names = [n for n,v in predicted_top_items[:7]]
        vals = [v for n,v in predicted_top_items[:7]]
        self.future_ax.bar(names, vals)
        self.future_ax.set_title("Predicted Top Menu Items")
        self.future_ax.set_ylabel("Projected Count")
        self.future_ax.set_xticklabels(names, rotation=0, ha='center')
        self.month_ax.tick_params(axis='x', labelsize=8)
        self.future_canvas.draw()


    def export_predictions(self):
        fname = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files","*.csv"),("All files","*.*")],
                                             title="Save predictions as...")
        if not fname:
            return
        try:
            with open(fname, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Predicted profit", f"{predicted_profit:.2f}"])
                writer.writerow([])
                writer.writerow(["Predicted top items","predicted"])
                for n,v in predicted_top_items:
                    writer.writerow([n,v])
                writer.writerow([])
                writer.writerow(["Predicted top ingredients","predicted"])
                for n,v in predicted_top_ingredients:
                    writer.writerow([n,v])
            messagebox.showinfo("Saved", f"Exported predictions to:\n{fname}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

# Run
def main():
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
