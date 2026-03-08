import tkinter as tk
from tkinter import messagebox, ttk
import requests
import webbrowser

class WalletWindow(tk.Frame):
    """멀티 윈도우(탭) 내에서 개별 xpub/주소를 관리하는 클래스"""
    def __init__(self, parent, identifier, lang='KO'):
        super().__init__(parent, bg='#0A0A0A')
        self.id = identifier
        self.lang = lang
        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        # 상단 요약 정보
        header = tk.Frame(self, bg='#1A1A1A', padx=20, pady=20)
        header.pack(fill="x", padx=20, pady=20)
        
        self.lbl_bal_title = tk.Label(header, text="보유 잔고" if self.lang=='KO' else "Total Balance", fg="#AAAAAA", bg="#1A1A1A")
        self.lbl_bal_title.pack(anchor="w")
        
        self.lbl_btc = tk.Label(header, text="0.00000000 BTC", font=("Verdana", 24, "bold"), fg="#F7931A", bg="#1A1A1A")
        self.lbl_btc.pack(anchor="w")

        # 기능 버튼부 (받기, 보내기, UTXO)
        btn_frame = tk.Frame(self, bg='#0A0A0A')
        btn_frame.pack(fill="x", padx=20)
        
        btns = [
            ("📥 받기" if self.lang=='KO' else "Receive", self.show_receive),
            ("📤 보내기" if self.lang=='KO' else "Send", lambda: messagebox.showinfo("Info", "Coming Soon")),
            ("🔍 UTXO", self.show_utxo)
        ]
        
        for text, cmd in btns:
            tk.Button(btn_frame, text=text, bg="#252525", fg="white", bd=0, padx=15, pady=5, command=cmd).pack(side="left", padx=5)

        # 최근 트랜잭션 표
        self.tree = ttk.Treeview(self, columns=("txid", "value"), show="headings", height=8)
        self.tree.heading("txid", text="TXID")
        self.tree.heading("value", text="BTC")
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

    def refresh_data(self):
        try:
            # mempool.space API 사용 (실제 서비스 시 Electrum 서버 연동 로직으로 대체 가능)
            res = requests.get(f"https://mempool.space/api/address/{self.id}").json()
            bal = (res['chain_stats']['funded_txo_sum'] - res['chain_stats']['spent_txo_sum']) / 100_000_000
            self.lbl_btc.config(text=f"{bal:.8f} BTC")
        except: pass

    def show_receive(self):
        messagebox.showinfo("Address", f"내 주소: {self.id}")

    def show_utxo(self):
        # UTXO 조회 기능
        try:
            utxos = requests.get(f"https://mempool.space/api/address/{self.id}/utxo").json()
            msg = "\n".join([f"TX: {u['txid'][:10]}... | Amt: {u['value']/100_000_000} BTC" for u in utxos])
            messagebox.showinfo("UTXO List", msg if msg else "No UTXOs found")
        except: pass

class CoconutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coconut Multi-Pro")
        self.root.geometry("1200x800")
        self.lang = 'KO'
        
        # 메인 메뉴 바 (Electrum 설정 등)
        menu_bar = tk.Menu(self.root)
        setting_menu = tk.Menu(menu_bar, tearoff=0)
        setting_menu.add_command(label="Electrum Server 연결", command=self.connect_node)
        setting_menu.add_command(label="언어 변경 (KO/EN)", command=self.toggle_lang)
        menu_bar.add_cascade(label="Settings", menu=setting_menu)
        self.root.config(menu=menu_bar)

        # 멀티 윈도우를 위한 노트북(탭) UI
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # 테스트용 두 개의 지갑 동시에 열기 (좌우/탭 비교 가능)
        self.add_wallet("bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh")
        self.add_wallet("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa") # 사토시 주소

    def add_wallet(self, xpub_or_addr):
        frame = WalletWindow(self.notebook, xpub_or_addr, self.lang)
        self.notebook.add(frame, text=f"Wallet: {xpub_or_addr[:8]}...")

    def connect_node(self):
        # 노드 연결 설정 팝업
        messagebox.showinfo("Node", "본인 노드 Electrum 서버 주소를 입력하세요.\n(예: 127.0.0.1:50001)")

    def toggle_lang(self):
        self.lang = 'EN' if self.lang == 'KO' else 'KO'
        messagebox.showinfo("Language", f"언어가 {self.lang}로 변경되었습니다. (재시작 필요)")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoconutApp(root)
    root.mainloop()