"""
Probe Sequence Matcher - GUI Application
Finds exact matches of probe sequences within a target nucleotide sequence
Supports both forward (5'→3') and reverse complement (3'→5') matching
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import csv
from typing import List, Dict, Tuple


class ProbeMatcherApp:
    """Main application class for Probe Sequence Matcher"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Probe Sequence Matcher")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Data storage
        self.probes = []  # List of dicts: {'name': str, 'sequence': str}
        self.matches = []  # List of match results
        self.probe_file_path = None
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Create and arrange all GUI elements"""
        
        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # ========== HEADER FRAME ==========
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.grid(row=0, column=0, sticky="ew")
        
        title_label = ttk.Label(
            header_frame, 
            text="🧬 Probe Sequence Matcher", 
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Find exact probe matches in target nucleotide sequences",
            font=("Arial", 9)
        )
        subtitle_label.pack()
        
        # ========== CONTROL FRAME ==========
        control_frame = ttk.LabelFrame(self.root, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        # Probe file upload section
        probe_frame = ttk.Frame(control_frame)
        probe_frame.pack(fill="x", pady=5)
        
        self.upload_btn = ttk.Button(
            probe_frame,
            text="📁 Upload Probe CSV",
            command=self.upload_probe_csv
        )
        self.upload_btn.pack(side="left", padx=5)
        
        self.probe_label = ttk.Label(
            probe_frame,
            text="No file uploaded",
            foreground="gray"
        )
        self.probe_label.pack(side="left", padx=10)
        
        # Target sequence input section
        seq_label = ttk.Label(control_frame, text="Target Nucleotide Sequence:")
        seq_label.pack(anchor="w", pady=(10, 2))
        
        # Scrolled text widget for sequence input
        self.seq_text = scrolledtext.ScrolledText(
            control_frame,
            height=6,
            width=80,
            wrap=tk.WORD,
            font=("Courier", 10)
        )
        self.seq_text.pack(fill="both", expand=True, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill="x", pady=5)
        
        self.search_btn = ttk.Button(
            button_frame,
            text="🔍 Search Matches",
            command=self.search_matches,
            state="disabled"
        )
        self.search_btn.pack(side="left", padx=5)
        
        self.save_btn = ttk.Button(
            button_frame,
            text="💾 Save Results",
            command=self.save_results,
            state="disabled"
        )
        self.save_btn.pack(side="left", padx=5)
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear All",
            command=self.clear_all
        )
        self.clear_btn.pack(side="left", padx=5)
        
        # Status label
        self.status_label = ttk.Label(
            button_frame,
            text="Ready",
            foreground="blue"
        )
        self.status_label.pack(side="right", padx=10)
        
        # ========== RESULTS FRAME ==========
        results_frame = ttk.LabelFrame(self.root, text="Match Results", padding="10")
        results_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Create Treeview for results
        columns = ("Probe Name", "Match Type", "Start Position", "End Position", "Matched Sequence")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # Define column headings and widths
        self.tree.heading("Probe Name", text="Probe Name")
        self.tree.heading("Match Type", text="Match Type")
        self.tree.heading("Start Position", text="Start Position")
        self.tree.heading("End Position", text="End Position")
        self.tree.heading("Matched Sequence", text="Matched Sequence")
        
        self.tree.column("Probe Name", width=150, anchor="w")
        self.tree.column("Match Type", width=100, anchor="center")
        self.tree.column("Start Position", width=120, anchor="center")
        self.tree.column("End Position", width=120, anchor="center")
        self.tree.column("Matched Sequence", width=300, anchor="w")
        
        # Add scrollbars
        vsb = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(results_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for tree and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Results summary label
        self.summary_label = ttk.Label(
            results_frame,
            text="No matches found yet",
            foreground="gray"
        )
        self.summary_label.grid(row=2, column=0, columnspan=2, pady=5)
        
    def is_valid_sequence(self, sequence: str) -> bool:
        """Check if sequence contains only valid nucleotides (A, T, G, C)"""
        valid_bases = set('ATGCatgc')
        return all(base in valid_bases for base in sequence)
    
    def upload_probe_csv(self):
        """Handle probe CSV file upload"""
        file_path = filedialog.askopenfilename(
            title="Select Probe CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Read CSV file
            self.probes = []
            invalid_probes = []
            
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                
                # Read first row to check if it's a header
                first_row = next(reader, None)
                if first_row is None:
                    messagebox.showerror("Error", "CSV file is empty.")
                    return
                
                # Check if first row looks like a header
                # (contains common header words or non-DNA sequences)
                is_header = any(
                    keyword in first_row[0].lower() or keyword in (first_row[1].lower() if len(first_row) > 1 else '')
                    for keyword in ['probe', 'name', 'sequence', 'id', 'label']
                )
                
                # If not a header, process it as data
                if not is_header and len(first_row) >= 2:
                    name = first_row[0].strip()
                    seq = first_row[1].strip().upper()
                    
                    if name and seq:
                        if self.is_valid_sequence(seq):
                            self.probes.append({'name': name, 'sequence': seq})
                        else:
                            invalid_probes.append((name, seq))
                
                # Process remaining rows
                for row_num, row in enumerate(reader, start=2):
                    if len(row) >= 2 and row[0].strip() and row[1].strip():
                        name = row[0].strip()
                        seq = row[1].strip().upper()
                        
                        if self.is_valid_sequence(seq):
                            self.probes.append({'name': name, 'sequence': seq})
                        else:
                            invalid_probes.append((name, seq))
            
            # Report results
            if not self.probes and not invalid_probes:
                messagebox.showerror("Error", "No valid probe data found in CSV file.")
                return
            
            if invalid_probes:
                invalid_list = '\n'.join([f"  • {name}: {seq}" for name, seq in invalid_probes[:5]])
                if len(invalid_probes) > 5:
                    invalid_list += f"\n  ... and {len(invalid_probes) - 5} more"
                
                message = f"Found {len(invalid_probes)} probe(s) with invalid sequences.\n\n"
                message += "Invalid probes (only A, T, G, C allowed):\n" + invalid_list
                
                if self.probes:
                    message += f"\n\n{len(self.probes)} valid probe(s) were loaded successfully."
                    messagebox.showwarning("Warning", message)
                else:
                    message += "\n\nNo valid probes found. Please check your CSV file."
                    messagebox.showerror("Error", message)
                    self.probe_label.config(text="Invalid sequences in file", foreground="red")
                    return
            
            self.probe_file_path = file_path
            file_name = file_path.split('/')[-1]
            self.probe_label.config(
                text=f"✓ {file_name} ({len(self.probes)} probes loaded)",
                foreground="green"
            )
            self.search_btn.config(state="normal")
            self.status_label.config(text=f"Loaded {len(self.probes)} probes", foreground="green")
            
            if not invalid_probes:
                messagebox.showinfo(
                    "Success",
                    f"Successfully loaded {len(self.probes)} probes from {file_name}"
                )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV file:\n{str(e)}")
            self.probe_label.config(text="Error loading file", foreground="red")
    
    def reverse_complement(self, sequence: str) -> str:
        """Calculate reverse complement of a DNA sequence"""
        complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        try:
            rev_comp = ''.join(complement[base] for base in reversed(sequence.upper()))
            return rev_comp
        except KeyError:
            # If invalid nucleotide found, return empty string
            return ""
    
    def find_matches(self, probe_seq: str, target_seq: str) -> List[Tuple[int, int, str]]:
        """
        Find all occurrences of probe_seq in target_seq
        Returns list of tuples: (start_pos, end_pos, match_type)
        Positions are 1-based
        """
        matches = []
        probe_upper = probe_seq.upper()
        target_upper = target_seq.upper()
        
        # Search for forward matches (5'→3')
        start = 0
        while True:
            pos = target_upper.find(probe_upper, start)
            if pos == -1:
                break
            matches.append((pos + 1, pos + len(probe_upper), "5′→3′"))
            start = pos + 1
        
        # Search for reverse complement matches (3'→5')
        rev_comp = self.reverse_complement(probe_seq)
        if rev_comp:
            start = 0
            while True:
                pos = target_upper.find(rev_comp, start)
                if pos == -1:
                    break
                matches.append((pos + 1, pos + len(rev_comp), "3′→5′"))
                start = pos + 1
        
        return matches
    
    def search_matches(self):
        """Main search function - find all probe matches in target sequence"""
        # Get target sequence
        target_seq = self.seq_text.get("1.0", tk.END).strip()
        target_seq = ''.join(target_seq.split())  # Remove all whitespace
        
        if not target_seq:
            messagebox.showwarning("Warning", "Please enter a target nucleotide sequence.")
            return
        
        if not self.probes:
            messagebox.showwarning("Warning", "Please upload a probe CSV file first.")
            return
        
        # Validate sequence contains only valid nucleotides
        valid_bases = set('ATGCatgc')
        if not all(base in valid_bases for base in target_seq):
            messagebox.showerror(
                "Error",
                "Target sequence contains invalid characters.\nOnly A, T, G, C are allowed."
            )
            return
        
        # Update status
        self.status_label.config(text="Searching...", foreground="orange")
        self.root.update_idletasks()
        
        # Perform search
        self.matches = []
        
        # Search each probe
        for probe in self.probes:
            probe_matches = self.find_matches(probe['sequence'], target_seq)
            
            for start, end, match_type in probe_matches:
                # Extract matched sequence from target
                matched_seq = target_seq[start-1:end].upper()
                
                self.matches.append({
                    'probe_name': probe['name'],
                    'match_type': match_type,
                    'start_pos': start,
                    'end_pos': end,
                    'matched_seq': matched_seq
                })
        
        # Update results display
        self._update_results()
    
    def _update_results(self):
        """Update GUI with search results"""
        # Clear existing results
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new results
        for match in self.matches:
            self.tree.insert("", tk.END, values=(
                match['probe_name'],
                match['match_type'],
                match['start_pos'],
                match['end_pos'],
                match['matched_seq']
            ))
        
        # Update summary
        if self.matches:
            self.summary_label.config(
                text=f"Found {len(self.matches)} match(es)",
                foreground="green"
            )
            self.save_btn.config(state="normal")
            self.status_label.config(
                text=f"Search complete: {len(self.matches)} matches found",
                foreground="green"
            )
        else:
            self.summary_label.config(
                text="No matches found",
                foreground="gray"
            )
            self.status_label.config(text="Search complete: No matches", foreground="blue")
    
    def save_results(self):
        """Save match results to CSV file"""
        if not self.matches:
            messagebox.showinfo("Info", "No results to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".csv",
            initialfile="probe_matches.csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    "Probe Name",
                    "Match Type",
                    "Start Position",
                    "End Position",
                    "Matched Sequence"
                ])
                
                # Write data
                for match in self.matches:
                    writer.writerow([
                        match['probe_name'],
                        match['match_type'],
                        match['start_pos'],
                        match['end_pos'],
                        match['matched_seq']
                    ])
            
            messagebox.showinfo(
                "Success",
                f"Results saved successfully to:\n{file_path}"
            )
            self.status_label.config(text="Results saved", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results:\n{str(e)}")
    
    def clear_all(self):
        """Clear all data and reset the application"""
        confirm = messagebox.askyesno(
            "Confirm Clear",
            "Are you sure you want to clear all data and results?"
        )
        
        if not confirm:
            return
        
        # Clear data
        self.probes = []
        self.matches = []
        self.probe_file_path = None
        
        # Clear GUI elements
        self.seq_text.delete("1.0", tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Reset labels and buttons
        self.probe_label.config(text="No file uploaded", foreground="gray")
        self.summary_label.config(text="No matches found yet", foreground="gray")
        self.status_label.config(text="Ready", foreground="blue")
        self.search_btn.config(state="disabled")
        self.save_btn.config(state="disabled")


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = ProbeMatcherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()