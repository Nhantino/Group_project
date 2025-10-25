# Quy định tạo Pull Request và Merge Code

## 1. Quy định chung

### 1.1. Trước khi tạo Pull Request
- Đảm bảo code đã được test kỹ trên máy local
- Code phải tuân thủ coding standards của dự án
- Không có conflict với nhánh main
- Đã cập nhật code mới nhất từ nhánh main về máy local

### 1.2. Tiêu đề Pull Request
- Sử dụng format rõ ràng: `[Loại] Mô tả ngắn gọn`
- Các loại phổ biến:
  - `[Feature]` - Thêm tính năng mới
  - `[Fix]` - Sửa lỗi
  - `[Update]` - Cập nhật code hiện có
  - `[Refactor]` - Tái cấu trúc code
  - `[Docs]` - Cập nhật tài liệu

**Ví dụ:**
```
[Feature] Thêm chức năng đăng nhập
[Fix] Sửa lỗi hiển thị danh sách sản phẩm
```

## 2. Nội dung Pull Request

### 2.1. Mô tả chi tiết
Pull Request phải bao gồm:

**a) Mục đích:**
- Giải thích lý do thay đổi
- Vấn đề đang được giải quyết

**b) Các thay đổi chính:**
- Liệt kê các file và chức năng đã thay đổi
- Giải thích logic của các thay đổi quan trọng

**c) Cách test:**
- Hướng dẫn cách test các thay đổi
- Các test case đã thực hiện

**d) Screenshots (nếu có):**
- Đính kèm ảnh minh họa cho các thay đổi giao diện

### 2.2. Template Pull Request
```markdown
## Mô tả
[Mô tả ngắn gọn về thay đổi]

## Loại thay đổi
- [ ] Feature mới
- [ ] Sửa lỗi
- [ ] Cập nhật code
- [ ] Tài liệu

## Các thay đổi chính
- Thay đổi 1
- Thay đổi 2
- Thay đổi 3

## Cách test
1. Bước 1
2. Bước 2
3. Kết quả mong đợi

## Checklist
- [ ] Code đã được test
- [ ] Code tuân thủ coding standards
- [ ] Đã cập nhật tài liệu (nếu cần)
- [ ] Không có conflict với main
```

## 3. Quy trình Review Code

### 3.1. Người review
- Ít nhất 1 người phải review và approve trước khi merge
- Reviewer cần kiểm tra:
  - Logic code có đúng không
  - Code có dễ đọc, dễ maintain không
  - Có tuân thủ coding standards không
  - Có test case đầy đủ không

### 3.2. Xử lý feedback
- Người tạo PR phải trả lời tất cả comments
- Sửa code theo góp ý hoặc giải thích lý do không sửa
- Push thêm commit để sửa các vấn đề được nêu ra

## 4. Quy định Merge Code

### 4.1. Điều kiện để Merge
Pull Request chỉ được merge khi:
- ✅ Có ít nhất 1 approval từ reviewer
- ✅ Tất cả comments đã được resolve
- ✅ Không có conflict với nhánh main
- ✅ CI/CD pipeline pass (nếu có)
- ✅ Code đã được test kỹ

### 4.2. Cách Merge
**Option 1: Merge Commit** (Khuyến nghị)
- Giữ lại toàn bộ lịch sử commit
- Tạo merge commit mới
- Phù hợp cho dự án cần theo dõi lịch sử chi tiết

**Option 2: Squash and Merge**
- Gộp tất cả commit thành 1 commit duy nhất
- Làm sạch lịch sử Git
- Phù hợp khi có nhiều commit nhỏ lẻ

**Option 3: Rebase and Merge**
- Đặt các commit lên đầu nhánh main
- Giữ lịch sử tuyến tính
- Phù hợp cho team có kinh nghiệm

### 4.3. Sau khi Merge
- Xóa branch đã merge (nếu không còn sử dụng)
- Thông báo cho team biết đã merge
- Cập nhật task/ticket tương ứng về trạng thái "Done"
- Pull code mới nhất về máy local

## 5. Lưu ý quan trọng

### 5.1. Tránh
- ❌ Merge code chưa được review
- ❌ Merge code có conflict
- ❌ Merge code chưa test
- ❌ Tạo PR quá lớn (quá nhiều thay đổi)

### 5.2. Nên làm
- ✅ Tạo PR nhỏ, tập trung vào 1 chức năng
- ✅ Review code của người khác thường xuyên
- ✅ Trả lời comments nhanh chóng
- ✅ Cập nhật PR thường xuyên để tránh conflict

## 6. Quy trình tổng quan

```
1. Tạo Pull Request từ branch → main
2. Assign reviewer
3. Reviewer review và comment
4. Tác giả sửa code theo feedback
5. Reviewer approve
6. Merge vào main
7. Xóa branch (nếu cần)
8. Pull code mới về local
```
