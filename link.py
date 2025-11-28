import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import webbrowser
import re

class LinkCoder:
    def __init__(self, root):
        self.root = root
        self.root.title("Codificador/Decodificador de Enlaces")
        self.root.geometry("900x700")
        self.root.configure(bg='#f3f4f6')
        self.root.minsize(820, 620)
        self.root.resizable(True, True)
        
        self.setup_ui()
        
    def derive_key(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'fixed_salt_12345',
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def setup_ui(self):
        # Paleta moderna
        self.theme = {
            'bg': '#f3f4f6',        # Gray 100
            'surface': '#ffffff',   # White
            'text': '#111827',      # Gray 900
            'muted': '#6b7280',     # Gray 500
            'primary': '#2563eb',   # Blue 600
            'success': '#16a34a',   # Green 600
            'danger': '#dc2626',    # Red 600
            'warning': '#f59e0b',   # Amber 500
            'accent': '#7c3aed'     # Violet 600
        }
        self.root.configure(bg=self.theme['bg'])

        # Header sobrio
        header = ctk.CTkFrame(self.root, height=72, fg_color="transparent")
        header.pack(fill="x", side="top")
        title = ctk.CTkLabel(header, text="Codificador/Decodificador de Enlaces", font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w", padx=24, pady=16)
        
        # Contenedor principal
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=20)

        # Card
        card = ctk.CTkFrame(main_frame, corner_radius=8, border_width=1, border_color="#1f2937")
        card.pack(fill=tk.BOTH, expand=False, padx=6, pady=6)

        # Campos
        password_label = ctk.CTkLabel(card, text="Contraseña", font=('Segoe UI', 12, 'bold'))
        password_label.pack(anchor='w', pady=(16, 0), padx=16)
        
        self.password_entry = ctk.CTkEntry(card, show="•", width=400,
                                       font=('Segoe UI', 11), placeholder_text="Ingresa la contraseña")
        self.password_entry.pack(pady=8, padx=16, fill=tk.X)

        link_label = ctk.CTkLabel(card, text="Enlace", font=('Segoe UI', 12, 'bold'))
        link_label.pack(anchor='w', pady=(12, 0), padx=16)
        
        self.link_entry = ctk.CTkEntry(card, width=400,
                                   font=('Segoe UI', 11), placeholder_text="Pega el enlace aquí")
        self.link_entry.pack(pady=8, padx=16, fill=tk.X)

        # Botones principales
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(pady=18, padx=16, fill=tk.X)
        
        encode_btn = ctk.CTkButton(button_frame, text="Codificar",
                               font=('Segoe UI', 11, 'bold'), fg_color="transparent", text_color=self.theme['primary'],
                               hover_color="#0b1220", border_width=1, border_color="#334155", command=self.encode_link)
        encode_btn.pack(side=tk.LEFT, padx=8)
        # CTkButton gestiona hover automáticamente
        
        decode_btn = ctk.CTkButton(button_frame, text="Decodificar",
                               font=('Segoe UI', 11, 'bold'), fg_color="transparent", text_color=self.theme['success'],
                               hover_color="#0b1220", border_width=1, border_color="#334155", command=self.decode_link)
        decode_btn.pack(side=tk.LEFT, padx=8)
        
        clear_btn = ctk.CTkButton(button_frame, text="Limpiar",
                              font=('Segoe UI', 11, 'bold'), fg_color="transparent", text_color=self.theme['danger'],
                              hover_color="#0b1220", border_width=1, border_color="#334155", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=8)

        help_btn = ctk.CTkButton(button_frame, text="Instrucciones",
                             font=('Segoe UI', 11, 'bold'), fg_color="transparent", text_color=self.theme['warning'],
                             hover_color="#0b1220", border_width=1, border_color="#334155", command=self.show_help)
        help_btn.pack(side=tk.LEFT, padx=8)

        # Resultado
        result_label = ctk.CTkLabel(card, text="Resultado", font=('Segoe UI', 12, 'bold'))
        result_label.pack(anchor='w', pady=(8, 0), padx=16)
        
        result_text_frame = ctk.CTkFrame(card, corner_radius=6, border_width=1, border_color="#1f2937")
        result_text_frame.pack(fill=tk.BOTH, expand=False, pady=10, padx=16)
        
        self.result_text = ctk.CTkTextbox(result_text_frame, height=140,
                                   font=('Segoe UI', 11), wrap='word')
        
        scrollbar = tk.Scrollbar(result_text_frame, orient=tk.VERTICAL,
                                 command=self.result_text._textbox.yview)
        self.result_text._textbox.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Links clickables (usar Text interno)
        self.result_text._textbox.tag_configure('link', foreground='#60a5fa', underline=1)
        self.result_text._textbox.tag_bind('link', '<Button-1>', self.open_link)
        self.result_text._textbox.tag_bind('link', '<Enter>', lambda e: self.result_text._textbox.config(cursor='hand2'))
        self.result_text._textbox.tag_bind('link', '<Leave>', lambda e: self.result_text._textbox.config(cursor=''))

        # Botones inferiores
        bottom_button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        bottom_button_frame.pack(fill=tk.X, pady=18)
        
        copy_btn = ctk.CTkButton(bottom_button_frame, text="Copiar resultado", command=self.copy_result,
                                 fg_color="transparent", text_color="#a78bfa", hover_color="#ede9fe",
                                 border_width=1, border_color="#334155")
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        info_btn = ctk.CTkButton(bottom_button_frame, text="Info", command=self.show_info,
                                 fg_color="transparent", text_color="#22c55e", hover_color="#d1fae5",
                                 border_width=1, border_color="#334155")
        info_btn.pack(side=tk.LEFT, padx=8)

        # Footer
        self.create_fancy_footer(main_frame)

    def create_fancy_footer(self, parent):
        """Footer moderno con línea en gradiente y texto sutil"""
        footer_frame = ctk.CTkFrame(parent, fg_color="transparent", height=70)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        footer_frame.pack_propagate(False)
        
        # Línea superior sutil
        top_line = ctk.CTkFrame(footer_frame, height=1, fg_color="#334155")
        top_line.pack(fill=tk.X)
        
        # Contenido del footer centrado
        content_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        content_frame.pack(expand=True, fill=tk.BOTH)
        
        footer_text = "Creado Por José desde Málaga"
        footer_label = ctk.CTkLabel(content_frame, text=footer_text,
                               font=('Segoe UI', 12, 'bold'), text_color="#9ca3af")
        footer_label.pack(pady=8)
        
        year_label = ctk.CTkLabel(content_frame, text="2025",
                             font=('Segoe UI', 10), text_color="#9ca3af")
        year_label.pack()
        
        def on_enter(e):
            footer_label.configure(text_color="#e5e7eb")
            year_label.configure(text_color="#e5e7eb")
        
        def on_leave(e):
            footer_label.configure(text_color="#9ca3af")
            year_label.configure(text_color="#9ca3af")
        
        for widget in (footer_frame, footer_label, year_label):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def style_button(self, btn, base, hover):
        """Aplica hover y colores a botones tk.Button"""
        btn.configure(bg=base, activebackground=hover)
        def _enter(_):
            btn.config(bg=hover)
        def _leave(_):
            btn.config(bg=base)
        btn.bind("<Enter>", _enter)
        btn.bind("<Leave>", _leave)

    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb

    def draw_gradient(self, canvas, color1, color2):
        """Dibuja un gradiente vertical en un Canvas"""
        canvas.delete('grad')
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w <= 0 or h <= 0:
            return
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)
        for i in range(h):
            ratio = i / h
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            canvas.create_line(0, i, w, i, fill=self._rgb_to_hex((r, g, b)), tag='grad')

    def show_info(self):
        """Muestra una ventana modal con información del autor"""
        # Crear ventana modal
        info_window = ctk.CTkToplevel(self.root)
        info_window.title("Información del Autor")
        info_window.geometry("400x260")
        info_window.resizable(False, False)
        info_window.transient(self.root)
        info_window.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(info_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=24)
        
        # Icono de información
        icon_label = ctk.CTkLabel(main_frame, text="ℹ️", font=('Segoe UI', 24))
        icon_label.pack(pady=(0, 12))
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Información del Autor", 
                              font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 16))
        
        # Información del autor
        author_label = ctk.CTkLabel(main_frame, text="Creado Por José desde Málaga", 
                               font=('Segoe UI', 12), text_color="#9ca3af")
        author_label.pack(pady=4)
        
        rights_label = ctk.CTkLabel(main_frame, text="Todos los derechos reservados al autor.", 
                               font=('Segoe UI', 11, 'italic'), text_color="#9ca3af")
        rights_label.pack(pady=4)
        
        # Año
        year_label = ctk.CTkLabel(main_frame, text="2025", 
                             font=('Segoe UI', 10), text_color="#94a3b8")
        year_label.pack(pady=8)
        
        # Botón de cerrar
        close_btn = ctk.CTkButton(main_frame, text="Cerrar", 
                             font=('Segoe UI', 11, 'bold'), fg_color="#ef4444", text_color="white",
                             hover_color="#dc2626", command=info_window.destroy)
        close_btn.pack(pady=14)
        
        # Centrar ventana en la pantalla
        info_window.update_idletasks()
        x = (info_window.winfo_screenwidth() // 2) - (info_window.winfo_width() // 2)
        y = (info_window.winfo_screenheight() // 2) - (info_window.winfo_height() // 2)
        info_window.geometry(f"+{x}+{y}")

    def is_url(self, text):
        """Verifica si el texto es una URL válida"""
        url_pattern = re.compile(
            r'^(https?://)?'  # http:// o https://
            r'([a-zA-Z0-9.-]+)'  # dominio
            r'(\.[a-zA-Z]{2,})'  # extensión
            r'(:[0-9]{1,5})?'  # puerto
            r'(/[^\s]*)?$'  # ruta
        )
        return bool(url_pattern.match(text))

    def open_link(self, event):
        """Abre el enlace en el navegador"""
        index = self.result_text._textbox.index(f"@{event.x},{event.y}")
        tags = self.result_text._textbox.tag_names(index)
        
        if "link" in tags:
            start = self.result_text._textbox.index(f"{index} linestart")
            end = self.result_text._textbox.index(f"{index} lineend")
            link_text = self.result_text._textbox.get(start, end).strip()
            
            if not link_text.startswith(('http://', 'https://')):
                link_text = 'https://' + link_text
            
            webbrowser.open_new(link_text)

    def make_links_clickable(self, text):
        """Convierte URLs en texto a links clickables"""
        self.result_text._textbox.delete(1.0, tk.END)
        
        url_pattern = re.compile(r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[^\s]*')
        
        last_end = 0
        for match in url_pattern.finditer(text):
            if match.start() > last_end:
                self.result_text._textbox.insert(tk.END, text[last_end:match.start()])
            
            link_text = match.group()
            self.result_text._textbox.insert(tk.END, link_text, "link")
            last_end = match.end()
        
        if last_end < len(text):
            self.result_text._textbox.insert(tk.END, text[last_end:])

    def encode_link(self):
        try:
            password = self.password_entry.get()
            link = self.link_entry.get()
            
            if not password or not link:
                messagebox.showerror("Error", "Completa todos los campos")
                return

            fernet = Fernet(self.derive_key(password))
            encoded_link = fernet.encrypt(link.encode())
            
            self.result_text._textbox.delete(1.0, tk.END)
            self.result_text._textbox.insert(1.0, encoded_link.decode())
            self.result_text._textbox.tag_remove("link", 1.0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al codificar: {str(e)}")

    def decode_link(self):
        try:
            password = self.password_entry.get()
            link = self.link_entry.get()
            
            if not password or not link:
                messagebox.showerror("Error", "Completa todos los campos")
                return

            fernet = Fernet(self.derive_key(password))
            decoded_link = fernet.decrypt(link.encode())
            decoded_text = decoded_link.decode()
            
            if self.is_url(decoded_text):
                self.make_links_clickable(decoded_text)
            else:
                self.result_text._textbox.delete(1.0, tk.END)
                self.result_text._textbox.insert(1.0, decoded_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al decodificar: {str(e)}")

    def copy_result(self):
        result = self.result_text._textbox.get(1.0, tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("Éxito", "Resultado copiado al portapapeles")

    def clear_all(self):
        """Limpia todos los campos"""
        self.password_entry.delete(0, tk.END)
        self.link_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)

    def show_help(self):
        help_text = """
INSTRUCCIONES DE USO:

🔒 CODIFICAR:
1. Ingresa una contraseña
2. Pega el enlace que quieres codificar
3. Haz clic en "Codificar"
4. Copia el resultado codificado

🔓 DECODIFICAR:
1. Ingresa la misma contraseña usada para codificar
2. Pega el enlace codificado
3. Haz clic en "Decodificar"
4. El enlace aparecerá como clickable

🗑️ LIMPIAR:
- Limpia todos los campos para empezar de nuevo

📋 COPIAR:
- Copia el resultado al portapapeles

📝 NOTAS:
- Usa la misma contraseña para codificar/decodificar
- Los enlaces decodificados son clickables
- Guarda tu contraseña de forma segura
        """
        messagebox.showinfo("Instrucciones", help_text)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = LinkCoder(root)
    root.mainloop()