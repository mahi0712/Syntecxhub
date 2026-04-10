import tkinter as tk

class ExpertSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expert System (Clickable UI)")

        # Rules
        self.rules = [
            (["fever", "cough"], "flu"),
            (["flu", "body_pain"], "severe_flu"),
            (["severe_flu"], "doctor_needed"),
            (["fever", "rash"], "measles"),
            (["headache", "nausea"], "migraine"),
        ]

        # Symptoms list
        self.symptoms = ["fever", "cough", "body_pain", "rash", "headache", "nausea"]

        self.check_vars = {}

        tk.Label(root, text="Select Symptoms:", font=("Arial", 12, "bold")).pack()

        # Checkboxes
        for sym in self.symptoms:
            var = tk.IntVar()
            chk = tk.Checkbutton(root, text=sym, variable=var)
            chk.pack(anchor="w")
            self.check_vars[sym] = var

        tk.Button(root, text="Diagnose", command=self.run).pack(pady=5)
        tk.Button(root, text="Reset", command=self.reset).pack()

        self.output = tk.Text(root, height=12, width=60)
        self.output.pack()

    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.root.update()
        self.root.after(500)

    def forward_chain(self, facts):
        while True:
            new_fact_added = False

            for cond, result in self.rules:
                if all(c in facts for c in cond):
                    if result not in facts:
                        facts.add(result)
                        self.log(f"Rule: IF {cond} → THEN {result}")
                        new_fact_added = True

            if not new_fact_added:
                break

        return facts

    def run(self):
        self.output.delete(1.0, tk.END)

        facts = set([sym for sym, var in self.check_vars.items() if var.get() == 1])

        self.log(f"Initial Facts: {facts}\n")

        final_facts = self.forward_chain(facts)

        self.log("\nFinal Conclusions:")
        for f in final_facts:
            self.log(f"✔ {f}")

    def reset(self):
        for var in self.check_vars.values():
            var.set(0)
        self.output.delete(1.0, tk.END)


root = tk.Tk()
app = ExpertSystemGUI(root)
root.mainloop()