import sqlite3  
from tkinter import Tk, Label, Button, StringVar, Entry, messagebox, ttk  


def create_database():
    conn = sqlite3.connect('nilai_pegawai.db')  
    cursor = conn.cursor()
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS nilai_pegawai(
                 id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 nama_pegawai TEXT, 
                 alamat TEXT,  
                 posisi TEXT,  
                 tahunmasuk INTEGER
               )
         ''')
    conn.commit()
    conn.close()


def fetch_data():
    conn = sqlite3.connect('nilai_pegawai.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nilai_pegawai')  
    rows = cursor.fetchall()
    conn.close()
    return rows


def save_to_database(nama, alamat, posisi, tahunmasuk):
    conn = sqlite3.connect('nilai_pegawai.db')
    cursor = conn.cursor()
    cursor.execute('''
                    INSERT INTO nilai_pegawai (nama_pegawai, alamat, posisi, tahunmasuk)
                    VALUES (?, ?, ?, ?) 
                  ''', (nama, alamat, posisi, tahunmasuk))
    conn.commit()
    conn.close()

# Fungsi untuk memperbarui data berdasarkan ID
def update_database(record_id, nama, alamat, posisi, tahunmasuk):
    conn = sqlite3.connect('nilai_pegawai.db')
    cursor = conn.cursor()
    cursor.execute('''
           UPDATE nilai_pegawai 
           SET nama_pegawai = ?, alamat = ?, posisi = ?, tahunmasuk = ?
           WHERE id = ?
           ''', (nama, alamat, posisi, tahunmasuk, record_id))
    conn.commit()
    conn.close()


def delete_database(record_id):
    conn = sqlite3.connect('nilai_pegawai.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_pegawai WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()


def submit():
    try:
        
        nama = nama_var.get()
        alamat = alamat_var.get()
        posisi = posisi_var.get()
        tahunmasuk = int(tahunmasuk_var.get())

        
        if not nama:
            raise Exception("Nama Pegawai tidak boleh kosong")

        
        save_to_database(nama, alamat, posisi, tahunmasuk)
        messagebox.showinfo("Sukses", "Data berhasil disimpan")

        
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Nilai tidak valid: {e}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fungsi yang dipanggil ketika tombol Update ditekan
def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data yang ingin diupdate")

        # Ambil input
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        alamat = alamat_var.get()
        posisi = posisi_var.get()
        tahunmasuk = int(tahunmasuk_var.get())

        # Validasi input
        if not nama:
            raise ValueError("Nama Pegawai tidak boleh kosong")

        # Update data ke database
        update_database(record_id, nama, alamat, posisi, tahunmasuk)
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fungsi untuk menghapus data
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data tabel yang ingin dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fungsi untuk mengosongkan input form
def clear_inputs():
    nama_var.set("")
    alamat_var.set("")
    posisi_var.set("")
    tahunmasuk_var.set("")
    selected_record_id.set("")

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():  # Hapus semua data di tabel
        tree.delete(row)
    for row in fetch_data():  # Tambahkan data terbaru ke tabel
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi form ketika memilih data di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        alamat_var.set(selected_row[2])
        posisi_var.set(selected_row[3])
        tahunmasuk_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI menggunakan Tkinter
root = Tk()
root.title("Pegawai")

# Variabel Tkinter untuk input form
nama_var = StringVar()
alamat_var = StringVar()
posisi_var = StringVar()
tahunmasuk_var = StringVar()
selected_record_id = StringVar()

# Input form
Label(root, text="Nama Pegawai").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Alamat").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=alamat_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Posisi").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=posisi_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Tahun Masuk").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=tahunmasuk_var).grid(row=3, column=1, padx=10, pady=5)

# Tombol
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel
columns = ("ID", "Nama Pegawai", "Alamat", "Posisi", "Tahun Masuk")
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Mengisi tabel dengan data
populate_table()

root.mainloop()
