"""
===============================================================================
MÓDULO: Indicador Visual
DESCRIÇÃO: Interface
===============================================================================
"""

import tkinter as tk
from datetime import datetime
import threading
import os

class VisualIndicator:
    """
    Janela com indicador visual e botão para controlar monitoramento.
    Ao fechar, salva os logs automaticamente.
    """
    
    def __init__(self, monitor=None):
        self.root = None
        self.is_running = False
        self.start_time = None
        self.time_label = None
        self.status_label = None
        self.btn_toggle = None
        self.monitor = monitor
        self.is_monitoring = False
        
    def start(self):
        """Inicia a janela indicadora"""
        try:
            self.root = tk.Tk()
            self.root.title("🔒 Proctoring System v0.3")
            self.root.geometry("450x250+10+10")
            self.root.attributes('-topmost', True)
            self.root.resizable(False, False)
            
            # Cor de fundo (verde = parado, vermelho = monitorando)
            self.root.configure(bg='#444444')
            
            # Título
            title = tk.Label(
                self.root,
                text="🔒 SISTEMA DE PROCTORING",
                font=("Arial", 16, "bold"),
                bg='#444444',
                fg='white'
            )
            title.pack(pady=10)
            
            # Status
            self.status_label = tk.Label(
                self.root,
                text="⏸️ AGUARDANDO INÍCIO",
                font=("Arial", 12, "bold"),
                bg='#444444',
                fg='#ffaa00'
            )
            self.status_label.pack(pady=5)
            
            # Tempo
            self.time_label = tk.Label(
                self.root,
                text="Tempo: 00:00",
                font=("Arial", 10),
                bg='#444444',
                fg='white'
            )
            self.time_label.pack(pady=5)
            
            # Botão Iniciar/Parar
            self.btn_toggle = tk.Button(
                self.root,
                text="▶️ INICIAR MONITORAMENTO",
                font=("Arial", 11, "bold"),
                bg='#00aa00',
                fg='white',
                command=self.toggle_monitoring,
                width=25,
                height=2
            )
            self.btn_toggle.pack(pady=10)
            
            # Instruções
            info = tk.Label(
                self.root,
                text="Ao fechar esta janela, os logs serão salvos automaticamente",
                font=("Arial", 8),
                bg='#444444',
                fg='#aaaaaa'
            )
            info.pack(pady=5)
            
            self.is_running = True
            
            # Evento de fechamento da janela
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            
            print("✅ Interface visual iniciada")
            print("   Clique em 'INICIAR MONITORAMENTO' para começar")
            print("   Ao fechar a janela, os logs serão salvos automaticamente")
            
            # Iniciar mainloop (bloqueante)
            self.root.mainloop()
            
        except Exception as e:
            print(f"⚠️  Erro na interface visual: {e}")
            self.is_running = False
    
    def toggle_monitoring(self):
        """Alterna entre iniciar e parar monitoramento"""
        if not self.is_monitoring:
            # INICIAR
            self.is_monitoring = True
            self.start_time = datetime.now()
            
            self.status_label.config(
                text="🔴 MONITORAMENTO ATIVO",
                fg='#ff4444'
            )
            
            self.btn_toggle.config(
                text="⏹️ PARAR MONITORAMENTO",
                bg='#cc0000'
            )
            
            self.root.configure(bg='#662222')
            
            # Chamar callback para iniciar monitoramento real
            if self.monitor and hasattr(self.monitor, 'start_monitoring'):
                self.monitor.start_monitoring()
            
            self._update_time()
            
            print("\n▶️ MONITORAMENTO INICIADO")
            
        else:
            # PARAR
            self.is_monitoring = False
            
            self.status_label.config(
                text="⏸️ MONITORAMENTO PARADO",
                fg='#ffaa00'
            )
            
            self.btn_toggle.config(
                text="▶️ INICIAR MONITORAMENTO",
                bg='#00aa00'
            )
            
            self.root.configure(bg='#444444')
            
            # Chamar callback para parar e salvar
            if self.monitor and hasattr(self.monitor, 'stop_monitoring'):
                self.monitor.stop_monitoring()
            
            print("\n⏹️ MONITORAMENTO PARADO - Logs salvos!")
    
    def _update_time(self):
        """Atualiza contador de tempo"""
        if self.is_running and self.is_monitoring and self.root:
            try:
                elapsed = datetime.now() - self.start_time
                minutes, seconds = divmod(int(elapsed.total_seconds()), 60)
                self.time_label.config(text=f"Tempo: {minutes:02d}:{seconds:02d}")
                self.root.after(1000, self._update_time)
            except:
                pass
    
    def on_close(self):
        """
        Chamado quando o usuário fecha a janela.
        Salva os logs automaticamente antes de fechar.
        """
        print("\n" + "=" * 70)
        print("🚫 JANELA FECHADA PELO USUÁRIO")
        print("=" * 70)
        
        # Se estava monitorando, para e salva
        if self.is_monitoring:
            print("\n💾 Salvando logs antes de fechar...")
            if self.monitor and hasattr(self.monitor, 'stop_monitoring'):
                self.monitor.stop_monitoring()
        
        # Para a interface
        self.is_running = False
        
        if self.root:
            try:
                self.root.destroy()
            except:
                pass
        
        print("✅ Janela fechada com segurança")
    
    def stop(self):
        """Para a janela indicadora"""
        self.is_running = False
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass