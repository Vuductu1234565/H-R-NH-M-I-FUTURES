import streamlit as st

# Hàm tính toán
def calculate_balance(balance_after, pnl):
    return balance_after - pnl

def calculate_leverage(pnl, entry_price, exit_price, margin, position_type):
    if entry_price <= 0 or margin <= 0:
        return "Giá vào lệnh và ký quỹ phải lớn hơn 0!"
    diff = exit_price - entry_price if position_type == "Long" else entry_price - exit_price
    if diff == 0:
        return "Giá vào và giá thoát không được bằng nhau!"
    leverage = pnl / (diff * (margin / entry_price))
    return leverage if 1 <= leverage <= 125 else "Đòn bẩy phải từ 1 đến 125!"

def calculate_entry_price(pnl, leverage, exit_price, margin, position_type):
    if leverage <= 0 or margin <= 0:
        return "Đòn bẩy và ký quỹ phải lớn hơn 0!"
    if position_type == "Long":
        entry_price = exit_price - (pnl / leverage) * (exit_price / margin)
    else:  # Short
        entry_price = exit_price + (pnl / leverage) * (exit_price / margin)
    return entry_price if entry_price > 0 else "Giá vào lệnh phải lớn hơn 0!"

def calculate_exit_price(entry_price, leverage, margin, pnl, position_type):
    if entry_price <= 0 or leverage <= 0 or margin <= 0:
        return "Giá vào, đòn bẩy, ký quỹ phải lớn hơn 0!"
    if position_type == "Long":
        exit_price = entry_price + (pnl / leverage) * (entry_price / margin)
    else:  # Short
        exit_price = entry_price - (pnl / leverage) * (entry_price / margin)
    return exit_price if exit_price > 0 else "Giá chốt lời phải lớn hơn 0!"

def calculate_margin(pnl, entry_price, exit_price, leverage, position_type):
    diff = exit_price - entry_price if position_type == "Long" else entry_price - exit_price
    if diff == 0 or leverage <= 0:
        return "Giá vào và giá thoát không được bằng nhau, đòn bẩy phải lớn hơn 0!"
    margin = (pnl / (diff * leverage)) * entry_price
    return margin if margin > 0 else "Ký quỹ phải lớn hơn 0!"

def calculate_pnl(entry_price, exit_price, margin, leverage, position_type):
    if entry_price <= 0 or margin <= 0 or leverage <= 0:
        return "Giá vào lệnh, ký quỹ và đòn bẩy phải lớn hơn 0!"
    if position_type == "Long":
        return (exit_price - entry_price) * (margin / entry_price) * leverage
    else:  # Short
        return (entry_price - exit_price) * (margin / entry_price) * leverage

def calculate_loss(entry_price, stop_loss_price, margin, leverage, position_type):
    if entry_price <= 0 or margin <= 0 or leverage <= 0 or stop_loss_price <= 0:
        return "Giá vào, ký quỹ, đòn bẩy và giá cắt lỗ phải lớn hơn 0!"
    if position_type == "Long" and stop_loss_price >= entry_price:
        return "Giá cắt lỗ phải nhỏ hơn giá vào lệnh khi Long!"
    if position_type == "Short" and stop_loss_price <= entry_price:
        return "Giá cắt lỗ phải lớn hơn giá vào lệnh khi Short!"
    if position_type == "Long":
        return (stop_loss_price - entry_price) * (margin / entry_price) * leverage
    else:  # Short
        return (entry_price - stop_loss_price) * (margin / entry_price) * leverage

def calculate_stop_loss(entry_price, leverage, margin, desired_loss, position_type):
    if entry_price <= 0 or leverage <= 0 or margin <= 0:
        return "Giá vào, đòn bẩy và ký quỹ phải lớn hơn 0!"
    if desired_loss >= 0:
        return "Mức lỗ phải là số âm!"
    if position_type == "Long":
        stop_loss_price = entry_price + (desired_loss / leverage) * (entry_price / margin)
    else:  # Short
        stop_loss_price = entry_price - (desired_loss / leverage) * (entry_price / margin)
    return stop_loss_price if stop_loss_price > 0 else "Giá cắt lỗ không hợp lệ!"

def calculate_liquidation(entry_price, leverage, margin, balance, margin_type, position_type):
    if entry_price <= 0 or leverage <= 0 or margin <= 0:
        return "Giá vào lệnh, đòn bẩy và ký quỹ phải lớn hơn 0!"
    if margin_type == "Cross" and balance <= 0:
        return "Vốn ban đầu phải lớn hơn 0 khi dùng ký quỹ chéo!"
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
    return liquidation_price if liquidation_price > 0 else "KHÔNG CÓ GIÁ THANH LÝ"

def calculate_profit_loss_ratio(pnl, loss):
    if loss == 0:
        return "Lỗ không được bằng 0 để tính tỷ lệ!"
    if pnl < 0 or loss > 0:
        return "Lời phải dương và Lỗ phải âm!"
    return pnl / abs(loss)

# Giao diện Streamlit
st.title("Hổ Rình Mồi Futures")

# Nhập liệu
margin_mode = st.radio("Chế độ ký quỹ", ["Isolated", "Cross"])
position_type = st.radio("Vị thế", ["Long", "Short"])
balance = st.number_input("Vốn ban đầu (USDT)", min_value=0.0, value=0.0)
balance_after = st.number_input("Vốn sau lệnh (USDT)", min_value=0.0, value=0.0)
entry_price = st.number_input("Giá vào lệnh (USDT)", min_value=0.0, value=0.0)
exit_price = st.number_input("Giá chốt lời (USDT)", min_value=0.0, value=0.0)
margin = st.number_input("Ký quỹ (USDT)", min_value=0.0, value=0.0)
leverage = st.slider("Đòn bẩy", min_value=1, max_value=125, value=1)
pnl = st.number_input("Lời (USDT)", value=0.0)
stop_loss_price = st.number_input("Giá cắt lỗ (USDT)", min_value=0.0, value=0.0)
loss = st.number_input("Lỗ (USDT)", value=0.0)

# Nút tính toán
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Tính Vốn ban đầu"):
        result = calculate_balance(balance_after, pnl)
        st.success(f"Vốn ban đầu: {result:.2f} USDT")
with col2:
    if st.button("Tính Đòn bẩy"):
        result = calculate_leverage(pnl, entry_price, exit_price, margin, position_type)
        if isinstance(result, str):
            st.error(result)
        else:
            st.success(f"Đòn bẩy: {result:.2f}x")
with col3:
    if st.button("Tính Giá vào lệnh"):
        result = calculate_entry_price(pnl, leverage, exit_price, margin, position_type)
        if isinstance(result, str):
            st.error(result)
        else:
            st.success(f"Giá vào lệnh: {result:.2f} USDT")

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("Tính Giá chốt lời"):
        result = calculate_exit_price(entry_price, leverage, margin, pnl, position_type)
        if isinstance(result, str):
            st.error(result)
        else:
            st.success(f"Giá chốt lời: {result:.2f} USDT")
with col5:
    if st.button("Tính Ký quỹ"):
        result = calculate_margin(pnl, entry_price, exit_price, leverage, position_type)
        if isinstance(result, str):
            st.error(result)
        else:
            st.success(f"Ký quỹ: {result:.2f} USDT")
with col6:
    if st.button("Tính PNL"):
        result = calculate_pnl(entry_price, exit_price, margin, leverage, position_type)
        if isinstance(result, str):
            st.error(result)
        else:
            st.success(f"Lời: {result:.2f} USDT")

col7, col8, col9 = st.columns(3)
with col7:
    if st.button("Tính Lỗ"):
        result = calculate_loss(entry_price, stop_loss_price, margin, leverage, position_type)
        if isinstance(result, str):
            st.error(result)
        else:
            st.success(f"Lỗ: {result:.2f} USDT")
with col8:
    if st.button("Tính Giá cắt lỗ"):
        result = calculate_stop_loss(entry_price, leverage, margin, loss, position_type)
        if isinstance(result, str):
            st.error(result)
        else:
            st.success(f"Giá cắt lỗ: {result:.2f} USDT")
with col9:
    if st.button("Tính Giá thanh lý"):
        result = calculate_liquidation(entry_price, leverage, margin, balance, margin_mode, position_type)
        if isinstance(result, str):
            st.error(result)
        else:
            st.success(f"Giá thanh lý: {result:.2f} USDT")

if st.button("Tính Tỷ lệ Lãi/Lỗ"):
    result = calculate_profit_loss_ratio(pnl, loss)
    if isinstance(result, str):
        st.error(result)
    else:
        st.success(f"Tỷ lệ Lãi/Lỗ: {result:.2f}")

# Hiển thị kết quả
st.write(f"Vốn sau lệnh: {balance + pnl:.2f} USDT")
st.write(f"Lời: {pnl:.2f} USDT")
st.write(f"Lỗ: {loss:.2f} USDT")