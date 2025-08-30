import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk

questions = {
    "Collaborative Leadership": [
        "I ensure project information is shared in a timely manner",
        "I prioritize developing strong team relationships",
        "I engage team members and stakeholders in decision making",
        "My team is empowered to operate independently",
        "We don’t avoid conflict, and we deal with it constructively"
    ],
    "Communication": [
        "I tailor my communication style to each audience’s needs",
        "I ask questions to test for understanding",
        "I keep communications as concise as possible",
        "I spend as much time listening as talking",
        "I correct communications mistakes as soon as possible"
    ],
    "Problem Solving": [
        "I create a trusting team environment, so I know about problems",
        "I am willing to make tough decisions when needed",
        "I work with my team to proactively prevent problems",
        "As a team we develop alternative approaches",
        "When decisions are taken, I ensure action steps are taken"
    ],
    "Strategic Thinking": [
        "I consider the business implications of every decision",
        "I understand the success criteria of my projects",
        "I ensure my team understands the project’s business purpose",
        "I adapt the triple constraint if it helps deliver project outcomes",
        "I ensure my actions align to the wider organizational strategy"
    ]
}

pm_guidance = {
    "Collaborative Leadership": ["Principle 2: Create a Collaborative Project Team Environment", "Team Performance Domain"],
    "Communication": ["Principle 3: Engage with Stakeholders", "Stakeholder Performance Domain"],
    "Problem Solving": ["Principle 6: Demonstrate Leadership Behaviors", "Planning & Project Work Domains"],
    "Strategic Thinking": ["Principle 4: Focus on Value", "Measurement & Delivery Domains"]
}

score_map = {"Always": 5, "Often": 4, "Sometimes": 3, "Seldom": 2, "Never": 1}

class PIMBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PIMBot - Power Skills Assessment")
        self.root.geometry("550x450")
        self.results = {}
        self.all_answers = []
        self.skill_list = list(questions.items())
        self.total_questions = sum(len(qs) for _, qs in self.skill_list)
        self.current_skill_index = 0
        self.q_index = 0

        self.start_screen()

    def start_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="PIMBot Power Skills Assessment", font=("Arial", 18, "bold"), pady=10).pack()
        tk.Label(
            self.root,
            text="Evaluate your leadership, communication, problem-solving, and strategic thinking skills based on PMI's PMBOK 7th Edition.",
            wraplength=500,
            justify="center",
            pady=10
        ).pack()
        tk.Button(self.root, text="Start Assessment", command=self.create_question_ui, width=20, height=2).pack(pady=20)

    def create_question_ui(self):
        self.clear_screen()
        self.current_skill, self.current_questions = self.skill_list[self.current_skill_index]

        question_text = self.current_questions[self.q_index]
        question_number = sum(len(qs) for _, qs in self.skill_list[:self.current_skill_index]) + self.q_index + 1

        tk.Label(self.root, text=f"Skill Area: {self.current_skill}", font=("Arial", 14, "bold"), pady=5).pack()
        tk.Label(self.root, text=f"Question {question_number} of {self.total_questions}", font=("Arial", 10)).pack()
        
        progress = ttk.Progressbar(self.root, length=500, mode='determinate')
        progress['value'] = (question_number / self.total_questions) * 100
        progress.pack(pady=5)

        tk.Label(self.root, text=question_text, wraplength=500, justify="left", pady=10).pack()

        for option in score_map.keys():
            tk.Button(self.root, text=option, width=20, command=lambda o=option: self.record_answer(o)).pack(pady=2)

    def record_answer(self, answer):
        score = score_map[answer]
        self.all_answers.append((self.current_skill, self.current_questions[self.q_index], score))
        self.q_index += 1
        if self.q_index >= len(self.current_questions):
            avg_score = sum(a[2] for a in self.all_answers if a[0] == self.current_skill) / len(self.current_questions)
            self.results[self.current_skill] = avg_score
            self.current_skill_index += 1
            self.q_index = 0
            if self.current_skill_index >= len(self.skill_list):
                self.show_results()
                return
        self.create_question_ui()

    def show_results(self):
        self.clear_screen()

        weakest_area = min(self.results, key=self.results.get)
        strongest_area = max(self.results, key=self.results.get)

        tk.Label(self.root, text="Assessment Complete", font=("Arial", 16, "bold"), pady=10).pack()

        for skill, score in self.results.items():
            focus = f" | Recommended Focus: {pm_guidance[skill][0]} ({pm_guidance[skill][1]})" if score < 4 else " | Maintain Excellence"
            tk.Label(self.root, text=f"{skill}: {score:.2f}/5{focus}", wraplength=500, justify="left").pack(pady=2)

        tk.Label(self.root, text=f"\nPrimary Focus Area for Improvement: {weakest_area} → {pm_guidance[weakest_area][0]}", wraplength=500, justify="left").pack()
        tk.Label(self.root, text=f"Strongest Area: {strongest_area} ({self.results[strongest_area]:.2f}/5) — Continue leveraging this strength.", wraplength=500, justify="left").pack(pady=5)

        with open("pimbot_assessment_report.txt", "w", encoding="utf-8") as f:
            f.write("PIMBot Power Skills Assessment Report\n" + "="*50 + "\n")
            for skill, score in self.results.items():
                f.write(f"{skill}: {score:.2f}/5\n")
            f.write(f"\nPrimary Focus Area: {weakest_area}\n")
            f.write(f"Strongest Area: {strongest_area}\n")

        tk.Button(self.root, text="Exit", command=self.root.destroy, width=20).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PIMBotUI(root)
    root.mainloop()
