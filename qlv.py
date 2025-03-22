import tkinter as tk
from tkinter import ttk, messagebox

def calculate_balance():
    try:
        pnl = float(pnl_var.get() or 0)
        balance_after = float(balance_after_var.get() or 0)
        balance_var.set(f"{balance_after - pnl:.2f}")
        update_labels()
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho vốn ban đầu!")

def calculate_leverage():
    try:
        position_type = position_var.get()
        pnl = float(pnl_var.get() or 0)
        entry_price = float(entry_price_var.get() or 0)
        exit_price = float(exit_price_var.get() or 0)
        margin = float(margin_var.get() or 0)
        if entry_price <= 0 or margin <= 0:
            raise ValueError("Giá vào lệnh và ký quỹ phải lớn hơn 0!")
        diff = exit_price - entry_price if position_type == "Long" else entry_price - exit_price
        if diff == 0:
            raise ValueError("Giá vào và giá thoát không được bằng nhau!")
        leverage = pnl / (diff * (margin / entry_price))
        if leverage <= 0 or leverage > 125:
            raise ValueError("Đòn bẩy phải từ 1 đến 125!")
        leverage_var.set(f"{leverage:.2f}")
        leverage_scale.set(leverage)
        update_labels()
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))

def calculate_entry_price():
    try:
        position_type = position_var.get()
        pnl = float(pnl_var.get() or 0)
        leverage = float(leverage_var.get() or 0)
        exit_price = float(exit_price_var.get() or 0)
        margin = float(margin_var.get() or 0)
        if leverage <= 0 or margin <= 0:
            raise ValueError("Đòn bẩy và ký quỹ phải lớn hơn 0!")
        if position_type == "Long":
            entry_price = exit_price - (pnl / leverage) * (entry_price_var.get() or 1) / margin
        else:  # Short
            entry_price = exit_price + (pnl / leverage) * (entry_price_var.get() or 1) / margin
        if entry_price <= 0:
            raise ValueError("Giá vào lệnh phải lớn hơn 0!")
        entry_price_var.set(f"{entry_price:.2f}")
        update_labels()
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))

def calculate_exit_price():
    try:
        position_type = position_var.get()
        entry_price = float(entry_price_var.get() or 0)
        exit_price = float(exit_price_var.get() or 0)
        leverage = float(leverage_var.get() or 0)
        margin = float(margin_var.get() or 0)
        if entry_price <= 0 or leverage <= 0 or margin <= 0 or exit_price <= 0:
            raise ValueError("Giá vào, đòn bẩy, ký quỹ và giá chốt lời phải lớn hơn 0!")
        if position_type == "Long" and exit_price <= entry_price:
            raise ValueError("Giá chốt lời phải lớn hơn giá vào lệnh khi Long!")
        if position_type == "Short" and exit_price >= entry_price:
            raise ValueError("Giá chốt lời phải nhỏ hơn giá vào lệnh khi Short!")
        if position_type == "Long":
            pnl = (exit_price - entry_price) * (margin / entry_price) * leverage
        else:  # Short
            pnl = (entry_price - exit_price) * (margin / entry_price) * leverage
        pnl_var.set(f"{pnl:.2f}")
        update_labels()
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))

def calculate_margin():
    try:
        position_type = position_var.get()
        pnl = float(pnl_var.get() or 0)
        leverage = float(leverage_var.get() or 0)
        entry_price = float(entry_price_var.get() or 0)
        exit_price = float(exit_price_var.get() or 0)
        if leverage <= 0 or entry_price <= 0:
            raise ValueError("Đòn bẩy và giá vào phải lớn hơn 0!")
        diff = exit_price - entry_price if position_type == "Long" else entry_price - exit_price
        if diff == 0:
            raise ValueError("Giá vào và giá thoát không được bằng nhau!")
        margin = (pnl / (diff * leverage)) * entry_price
        if margin <= 0:
            raise ValueError("Ký quỹ phải lớn hơn 0!")
        margin_var.set(f"{margin:.2f}")
        update_labels()
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))

def calculate_pnl():
    try:
        position_type = position_var.get()
        leverage = float(leverage_var.get() or 0)
        entry_price = float(entry_price_var.get() or 0)
        exit_price = float(exit_price_var.get() or 0)
        margin = float(margin_var.get() or 0)
        if entry_price <= 0 or margin <= 0 or leverage <= 0:
            raise ValueError("Giá vào lệnh, ký quỹ và đòn bẩy phải lớn hơn 0!")
        if position_type == "Long":
            pnl = (exit_price - entry_price) * (margin / entry_price) * leverage
        else:  # Short
            pnl = (entry_price - exit_price) * (margin / entry_price) * leverage
        pnl_var.set(f"{pnl:.2f}")
        update_labels()
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))

def calculate_loss():
    try:
        position_type = position_var.get()
        leverage = float(leverage_var.get() or 0)
        entry_price = float(entry_price_var.get() or 0)
        stop_loss_price = float(stop_loss_var.get() or 0)
        margin = float(margin_var.get() or 0)
        if entry_price <= 0 or margin <= 0 or leverage <= 0 or stop_loss_price <= 0:
            raise ValueError("Giá vào, ký quỹ, đòn bẩy và giá cắt lỗ phải lớn hơn 0!")
        if position_type == "Long" and stop_loss_price >= entry_price:
            raise ValueError("Giá cắt lỗ phải nhỏ hơn giá vào lệnh khi Long!")
        if position_type == "Short" and stop_loss_price <= entry_price:
            raise ValueError("Giá cắt lỗ phải lớn hơn giá vào lệnh khi Short!")
        if position_type == "Long":
            loss = (stop_loss_price - entry_price) * (margin / entry_price) * leverage
        else:  # Short
            loss = (entry_price - stop_loss_price) * (margin / entry_price) * leverage
        loss_var.set(f"{loss:.2f}")
        update_labels()
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))

def calculate_stop_loss():
    try:
        position_type = position_var.get()
        entry_price = float(entry_price_var.get() or 0)
        leverage = float(leverage_var.get() or 0)
        margin = float(margin_var.get() or 0)
        desired_loss = float(loss_var.get() or 0)
        if entry_price <= 0 or leverage <= 0 or margin <= 0:
            raise ValueError("Giá vào, đòn bẩy và ký quỹ phải lớn hơn 0!")
        if desired_loss >= 0:
            raise ValueError("Mức lỗ phải là số âm!")
        if position_type == "Long":
            stop_loss_price = entry_price + (desired_loss / leverage) * (entry_price / margin)
        else:  # Short
            stop_loss_price = entry_price - (desired_loss / leverage) * (entry_price / margin)
        if stop_loss_price <= 0:
            raise ValueError("Giá cắt lỗ không hợp lệ (âm hoặc bằng 0)!")
        stop_loss_var.set(f"{stop_loss_price:.2f}")
        update_labels()
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))

def calculate_liquidation():
    try:
        position_type = position_var.get()
        margin_type = margin_mode_var.get()
        entry_price = float(entry_price_var.get() or 0)
        leverage = float(leverage_var.get() or 0)
        margin = float(margin_var.get() or 0)
        balance = float(balance_var.get() or 0)
        if entry_price <= 0 or leverage <= 0 or margin <= 0:
            raise ValueError("Giá vào lệnh, đòn bẩy và ký quỹ phải lớn hơn 0!")
        if margin_type == "Cross" and balance <= 0:
            raise ValueError("Vốn ban đầu phải lớn hơn 0 khi dùng ký quỹ chéo!")
        if margin_type == "Isolated":
            if position_type == "Long":
                liquidation_price = entry_price * (1 - 1 / leverage)
            else:  # Short
                liquidation_price = entry_price * (1 + 1 / leverage)
        else:  # Cross
            if position_type == "Long":
                liquidation_price = entry_price - (balance * entry_price) / (margin * leverage)
            else:  # Short
                liquidation_price = entry_price + (balance * entry_price) / (margin * leverage)
        # Kiểm tra giá thanh lý dự kiến có hợp lệ không
        if liquidation_price <= 0:
            liquidation_var.set("KHÔNG CÓ GIÁ THANH LÝ")  # Hiển thị thông báo thay vì 0
            raise ValueError("Giá thanh lý dự kiến không hợp lệ!")
        liquidation_var.set(f"{liquidation_price:.2f}")
        update_labels()
    except ValueError as e:
        liquidation_var.set("KHÔNG CÓ GIÁ THANH LÝ")  # Hiển thị thông báo nếu có lỗi
        messagebox.showerror("Lỗi", str(e))

def calculate_profit_loss_ratio():
    try:
        profit = float(pnl_var.get() or 0)
        loss = float(loss_var.get() or 0)
        if loss == 0:
            raise ValueError("Lỗ không được bằng 0 để tính tỷ lệ!")
        if profit < 0 or loss > 0:
            raise ValueError("Lời phải dương và Lỗ phải âm!")
        ratio = profit / abs(loss)
        profit_loss_ratio_var.set(f"{ratio:.2f}")
        update_labels()
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))

def update_labels():
    try:
        balance = float(balance_var.get() or 0)
        pnl = float(pnl_var.get() or 0)
        loss = float(loss_var.get() or 0)
        ratio = float(profit_loss_ratio_var.get() or 0)
        balance_after_var.set(f"{balance + pnl:.2f}")
        balance_after_label.config(text=f"Vốn sau lệnh: {balance + pnl:,.2f} USDT")
        pnl_label.config(text=f"Lời: {pnl:,.2f} USDT")
        loss_label.config(text=f"Lỗ: {loss:,.2f} USDT")
        profit_loss_ratio_label.config(text=f"Tỷ lệ Lãi/Lỗ: {ratio:.2f}")
    except ValueError:
        profit_loss_ratio_label.config(text="Tỷ lệ Lãi/Lỗ: N/A")

def update_leverage_from_entry(*args):
    try:
        leverage = float(leverage_var.get() or 0)
        if 1 <= leverage <= 125:
            leverage_scale.set(leverage)
        else:
            leverage_var.set("")
            leverage_scale.set(1)
    except ValueError:
        leverage_var.set("")
        leverage_scale.set(1)

def update_leverage_from_scale(*args):
    leverage_var.set(str(leverage_scale.get()))

# Tạo cửa sổ chính
try:
    window = tk.Tk()
    window.title("Hổ Rình Mồi Futures")
    window.geometry("350x650")
    window.configure(bg="#f0f3f5")

    # Biến để lưu giá trị
    margin_mode_var = tk.StringVar(value="Isolated")
    position_var = tk.StringVar(value="Long")
    leverage_var = tk.StringVar(value="")
    entry_price_var = tk.StringVar(value="")
    exit_price_var = tk.StringVar(value="")
    margin_var = tk.StringVar(value="")
    balance_var = tk.StringVar(value="")
    pnl_var = tk.StringVar(value="")
    balance_after_var = tk.StringVar(value="")
    stop_loss_var = tk.StringVar(value="")
    liquidation_var = tk.StringVar(value="")
    loss_var = tk.StringVar(value="")
    profit_loss_ratio_var = tk.StringVar(value="")

    # Tiêu đề
    title_label = tk.Label(window, text="Hổ Rình Mồi Futures", font=("Arial", 16, "bold"), bg="#f0f3f5")
    title_label.pack(pady=10)

    # Chọn chế độ ký quỹ
    margin_mode_frame = ttk.Frame(window)
    margin_mode_frame.pack(pady=5)
    cross_button = tk.Radiobutton(margin_mode_frame, text="Ký quỹ chéo", variable=margin_mode_var, value="Cross", font=("Arial", 10), bg="#34c759", fg="white", selectcolor="#34c759", activebackground="#34c759")
    cross_button.pack(side=tk.LEFT, padx=5)
    isolated_button = tk.Radiobutton(margin_mode_frame, text="Ký quỹ riêng biệt", variable=margin_mode_var, value="Isolated", font=("Arial", 10), bg="#d3d7dc", fg="black", selectcolor="#d3d7dc", activebackground="#d3d7dc")
    isolated_button.pack(side=tk.LEFT, padx=5)

    # Chọn Long/Short
    position_frame = ttk.Frame(window)
    position_frame.pack(pady=5)
    long_button = tk.Radiobutton(position_frame, text="Long", variable=position_var, value="Long", font=("Arial", 10), bg="#34c759", fg="white", selectcolor="#34c759", activebackground="#34c759")
    long_button.pack(side=tk.LEFT, padx=5)
    short_button = tk.Radiobutton(position_frame, text="Short", variable=position_var, value="Short", font=("Arial", 10), bg="#d3d7dc", fg="black", selectcolor="#d3d7dc", activebackground="#d3d7dc")
    short_button.pack(side=tk.LEFT, padx=5)

    # Vốn ban đầu
    balance_frame = tk.Frame(window, bg="#f0f3f5")
    balance_frame.pack(pady=5)
    tk.Label(balance_frame, text="Vốn ban đầu (USDT):", bg="#f0f3f5").pack(side=tk.LEFT)
    balance_entry = tk.Entry(balance_frame, textvariable=balance_var, justify="right", width=15)
    balance_entry.pack(side=tk.LEFT)
    tk.Button(balance_frame, text="Tính", command=calculate_balance, bg="#34c759", fg="white").pack(side=tk.LEFT, padx=5)

    # Đòn bẩy
    leverage_frame = tk.Frame(window, bg="#f0f3f5")
    leverage_frame.pack(pady=5)
    tk.Label(leverage_frame, text="Đòn bẩy:", bg="#f0f3f5").pack(side=tk.LEFT)
    leverage_entry = tk.Entry(leverage_frame, textvariable=leverage_var, justify="right", width=10)
    leverage_entry.pack(side=tk.LEFT)
    tk.Label(leverage_frame, text="x", bg="#f0f3f5").pack(side=tk.LEFT, padx=2)
    tk.Button(leverage_frame, text="Tính", command=calculate_leverage, bg="#34c759", fg="white").pack(side=tk.LEFT, padx=5)
    leverage_scale = tk.Scale(window, from_=1, to=125, orient=tk.HORIZONTAL, variable=leverage_var, showvalue=0, resolution=1, bg="#f0f3f5", command=update_leverage_from_scale)
    leverage_scale.set(1)
    leverage_scale.pack()
    leverage_var.trace("w", update_leverage_from_entry)

    # Giá vào lệnh
    entry_price_frame = tk.Frame(window, bg="#f0f3f5")
    entry_price_frame.pack(pady=5)
    tk.Label(entry_price_frame, text="Giá vào lệnh (USDT):", bg="#f0f3f5").pack(side=tk.LEFT)
    entry_price_entry = tk.Entry(entry_price_frame, textvariable=entry_price_var, justify="right", width=15)
    entry_price_entry.pack(side=tk.LEFT)
    tk.Button(entry_price_frame, text="Tính", command=calculate_entry_price, bg="#34c759", fg="white").pack(side=tk.LEFT, padx=5)

    # Giá cắt lỗ
    stop_loss_frame = tk.Frame(window, bg="#f0f3f5")
    stop_loss_frame.pack(pady=5)
    tk.Label(stop_loss_frame, text="Giá cắt lỗ (USDT):", bg="#f0f3f5").pack(side=tk.LEFT)
    stop_loss_entry = tk.Entry(stop_loss_frame, textvariable=stop_loss_var, justify="right", width=15)
    stop_loss_entry.pack(side=tk.LEFT)
    tk.Button(stop_loss_frame, text="Tính", command=calculate_stop_loss, bg="#34c759", fg="white").pack(side=tk.LEFT, padx=5)

    # Giá chốt lời
    exit_price_frame = tk.Frame(window, bg="#f0f3f5")
    exit_price_frame.pack(pady=5)
    tk.Label(exit_price_frame, text="Giá chốt lời (USDT):", bg="#f0f3f5").pack(side=tk.LEFT)
    exit_price_entry = tk.Entry(exit_price_frame, textvariable=exit_price_var, justify="right", width=15)
    exit_price_entry.pack(side=tk.LEFT)
    tk.Button(exit_price_frame, text="Tính", command=calculate_exit_price, bg="#34c759", fg="white").pack(side=tk.LEFT, padx=5)

    # Ký quỹ
    margin_frame = tk.Frame(window, bg="#f0f3f5")
    margin_frame.pack(pady=5)
    tk.Label(margin_frame, text="Ký quỹ (USDT):", bg="#f0f3f5").pack(side=tk.LEFT)
    margin_entry = tk.Entry(margin_frame, textvariable=margin_var, justify="right", width=15)
    margin_entry.pack(side=tk.LEFT)
    tk.Button(margin_frame, text="Tính", command=calculate_margin, bg="#34c759", fg="white").pack(side=tk.LEFT, padx=5)

    # Lời
    pnl_frame = tk.Frame(window, bg="#f0f3f5")
    pnl_frame.pack(pady=5)
    tk.Label(pnl_frame, text="Lời (USDT):", bg="#f0f3f5").pack(side=tk.LEFT)
    pnl_entry = tk.Entry(pnl_frame, textvariable=pnl_var, justify="right", width=15)
    pnl_entry.pack(side=tk.LEFT)
    tk.Button(pnl_frame, text="Tính", command=calculate_pnl, bg="#34c759", fg="white").pack(side=tk.LEFT, padx=5)

    # Lỗ
    loss_frame = tk.Frame(window, bg="#f0f3f5")
    loss_frame.pack(pady=5)
    tk.Label(loss_frame, text="Lỗ (USDT):", bg="#f0f3f5").pack(side=tk.LEFT)
    loss_entry = tk.Entry(loss_frame, textvariable=loss_var, justify="right", width=15)
    loss_entry.pack(side=tk.LEFT)
    tk.Button(loss_frame, text="Tính", command=calculate_loss, bg="#34c759", fg="white").pack(side=tk.LEFT, padx=5)

    # Giá thanh lý dự kiến
    liquidation_frame = tk.Frame(window, bg="#f0f3f5")
    liquidation_frame.pack(pady=5)
    tk.Label(liquidation_frame, text="Giá thanh lý dự kiến (USDT):", bg="#f0f3f5").pack(side=tk.LEFT)
    liquidation_entry = tk.Entry(liquidation_frame, textvariable=liquidation_var, justify="right", width=15)
    liquidation_entry.pack(side=tk.LEFT)
    tk.Button(liquidation_frame, text="Tính", command=calculate_liquidation, bg="#34c759", fg="white").pack(side=tk.LEFT, padx=5)

    # Tỷ lệ Lãi/Lỗ
    profit_loss_ratio_frame = tk.Frame(window, bg="#f0f3f5")
    profit_loss_ratio_frame.pack(pady=5)
    tk.Label(profit_loss_ratio_frame, text="Tỷ lệ Lãi/Lỗ:", bg="#f0f3f5").pack(side=tk.LEFT)
    profit_loss_ratio_entry = tk.Entry(profit_loss_ratio_frame, textvariable=profit_loss_ratio_var, justify="right", width=15)
    profit_loss_ratio_entry.pack(side=tk.LEFT)
    tk.Button(profit_loss_ratio_frame, text="Tính", command=calculate_profit_loss_ratio, bg="#34c759", fg="white").pack(side=tk.LEFT, padx=5)

    # Kết quả
    pnl_label = tk.Label(window, text="Lời: 0.00 USDT", bg="#f0f3f5", font=("Arial", 10))
    pnl_label.pack(pady=5)
    loss_label = tk.Label(window, text="Lỗ: 0.00 USDT", bg="#f0f3f5", font=("Arial", 10))
    loss_label.pack(pady=5)
    balance_after_label = tk.Label(window, text="Vốn sau lệnh: 0.00 USDT", bg="#f0f3f5", font=("Arial", 10))
    balance_after_label.pack(pady=5)
    profit_loss_ratio_label = tk.Label(window, text="Tỷ lệ Lãi/Lỗ: N/A", bg="#f0f3f5", font=("Arial", 10))
    profit_loss_ratio_label.pack(pady=5)

    # Chạy ứng dụng
    window.mainloop()

except Exception as e:
    print(f"Lỗi khởi tạo: {e}")
    input("Nhấn Enter để thoát...")
