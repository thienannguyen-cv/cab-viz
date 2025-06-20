import os
import json
import re

def create_manifest(directory="."):
    """
    Quét một thư mục để tìm các cặp ảnh output/target và tạo ra file manifest.json.

    Hàm này sẽ tìm tất cả các file có định dạng '{epoch}_output.png' và kiểm tra
    xem có file '{epoch}_target.png' tương ứng hay không.
    """
    epoch_data = {}
    
    # Biểu thức chính quy để trích xuất số epoch từ tên file
    output_pattern = re.compile(r"(\d+)_output\.png")

    print(f"Bắt đầu quét thư mục: '{os.path.abspath(directory)}'")

    # Duyệt qua tất cả các file trong thư mục được chỉ định
    for filename in os.listdir(directory):
        match = output_pattern.match(filename)
        if match:
            epoch_number = int(match.group(1))
            
            # Tạo tên file output và target tương ứng
            output_file = filename
            target_file = f"{epoch_number}_target.png"

            # Kiểm tra xem file target tương ứng có tồn tại không
            if os.path.exists(os.path.join(directory, target_file)):
                # Nếu cả hai file đều tồn tại, thêm vào danh sách
                if epoch_number not in epoch_data:
                    epoch_data[epoch_number] = {
                        "epoch": epoch_number,
                        "output": output_file,
                        "target": target_file
                    }
                print(f"  -> Tìm thấy cặp hợp lệ cho Epoch {epoch_number}: '{output_file}', '{target_file}'")
            else:
                print(f"  -> Cảnh báo: Tìm thấy '{output_file}' nhưng không có '{target_file}'. Bỏ qua.")

    # Chuyển đổi từ điển thành một danh sách và sắp xếp theo số epoch
    manifest_list = sorted(epoch_data.values(), key=lambda x: x['epoch'])
    
    # Ghi danh sách đã sắp xếp vào file manifest.json
    manifest_path = os.path.join(directory, 'manifest.json')
    try:
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_list, f, indent=2, ensure_ascii=False)
        print(f"\nThành công! Đã tạo file 'manifest.json' với {len(manifest_list)} mục.")
    except IOError as e:
        print(f"\nLỗi: Không thể ghi file 'manifest.json'. Lý do: {e}")


if __name__ == "__main__":
    # Chạy hàm với thư mục hiện tại
    create_manifest()

