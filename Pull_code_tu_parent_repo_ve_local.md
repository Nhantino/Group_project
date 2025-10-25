# Hướng dẫn Pull Code từ Parent Repo về Local

## Phương án 1: Sử dụng Git Command Line

### Bước 1: Kiểm tra trạng thái hiện tại
```bash
# Kiểm tra branch hiện tại
git branch

# Đảm bảo đang ở nhánh main
# Nếu không, chuyển về main:
git checkout main

# Kiểm tra có thay đổi chưa commit không
git status
```

### Bước 2: Lưu thay đổi đang làm (nếu có)

**Option A: Commit thay đổi**
```bash
git add .
git commit -m "Work in progress"
```

**Option B: Stash thay đổi (cất tạm thời)**
```bash
# Cất thay đổi vào stash
git stash

# Sau khi pull xong, lấy lại:
git stash pop
```

### Bước 3: Pull code từ parent repo
```bash
# Pull code từ nhánh main
git pull origin main

# Lệnh này tương đương với:
# git fetch origin
# git merge origin/main
```

**Kết quả có thể xảy ra:**

**Trường hợp 1: Pull thành công (Fast-forward)**
```
Updating abc1234..def5678
Fast-forward
 file1.js | 10 ++++++++++
 file2.js |  5 +++--
 2 files changed, 13 insertions(+), 2 deletions(-)
```

**Trường hợp 2: Có conflict**
```
Auto-merging file1.js
CONFLICT (content): Merge conflict in file1.js
Automatic merge failed; fix conflicts and then commit the result.
```

### Bước 4: Xử lý conflict (nếu có)

**A. Kiểm tra file có conflict:**
```bash
git status
```

**B. Mở file conflict và tìm các marker:**
```javascript
<<<<<<< HEAD
// Code của bạn trên local
const name = "Local";
=======
// Code từ remote
const name = "Remote";
>>>>>>> origin/main
```

**C. Sửa file:**
- Chọn giữ code nào: local, remote, hoặc kết hợp cả hai
- Xóa các dấu marker (`<<<<<<<`, `=======`, `>>>>>>>`)
- Lưu file

**D. Hoàn thành resolve conflict:**
```bash
# Add file đã sửa
git add <tên-file>

# Commit merge
git commit -m "Resolve merge conflict"

# Kiểm tra status
git status
```

### Bước 5: Xác nhận đã pull thành công
```bash
# Xem commit mới nhất
git log -3

# Xem chi tiết thay đổi
git log --oneline --graph -5

# So sánh với remote
git status
```

---

## Phương án 2: Sử dụng GitHub Desktop

### Bước 1: Mở GitHub Desktop
- Mở ứng dụng GitHub Desktop
- Chọn repository đang làm việc
- Đảm bảo đang ở nhánh "main" (hiển thị ở trên cùng)

### Bước 2: Lưu thay đổi đang làm (nếu có)
- Nếu có thay đổi chưa commit:
  - Điền commit message ở góc dưới trái
  - Click "Commit to main"
- Hoặc có thể stash thay đổi:
  - Branch → Stash all changes

### Bước 3: Fetch thông tin từ remote
- Click nút "Fetch origin" ở thanh công cụ trên cùng
- GitHub Desktop sẽ kiểm tra xem có code mới không

**Các trạng thái có thể gặp:**

**Trạng thái 1: "Pull origin"**
- Có code mới từ remote
- Click "Pull origin" để tải về

**Trạng thái 2: "Push origin"**
- Local có code mới hơn remote
- Không cần pull

**Trạng thái 3: Không có gì**
- Local và remote đã đồng bộ

### Bước 4: Pull code về
- Click nút "Pull origin"
- Chờ progress bar hoàn thành
- GitHub Desktop sẽ tự động merge code

### Bước 5: Xử lý conflict (nếu có)
- Nếu có conflict, GitHub Desktop sẽ hiển thị thông báo
- Click "Open in [your editor]" để mở file conflict
- Sửa conflict trong editor
- Lưu file và quay lại GitHub Desktop
- Click "Continue merge" hoặc "Commit merge"

### Bước 6: Xác nhận
- Kiểm tra tab "History" để xem commit mới
- Panel bên phải sẽ hiển thị các thay đổi

---

## Quy trình làm việc khuyến nghị

### Khi bắt đầu ngày làm việc:
```bash
# 1. Pull code mới nhất
git pull origin main

# 2. Kiểm tra có cập nhật gì
git log -3

# 3. Bắt đầu code
```

### Trước khi push code:
```bash
# 1. Pull code mới để tránh conflict
git pull origin main

# 2. Test code sau khi merge
npm test  # hoặc lệnh test tương ứng

# 3. Push code
git push origin main
```

### Định kỳ trong ngày:
```bash
# Pull code mỗi 1-2 giờ để tránh conflict lớn
git pull origin main
```

---

## Các lệnh Git nâng cao

### Kiểm tra thông tin remote
```bash
# Xem remote repository
git remote -v

# Xem thông tin chi tiết về remote
git remote show origin

# Kiểm tra local có đồng bộ với remote không
git fetch origin
git status
```

### Pull với các option khác nhau

**Pull và rebase (thay vì merge):**
```bash
git pull --rebase origin main
```
- Ưu điểm: Lịch sử commit sạch hơn, tuyến tính
- Nhược điểm: Có thể phức tạp hơn khi có conflict

**Pull và tự động stash:**
```bash
git pull --autostash origin main
```
- Tự động stash thay đổi trước khi pull
- Tự động apply stash lại sau khi pull

**Fetch without merge:**
```bash
# Chỉ tải thông tin về, không merge
git fetch origin

# Xem có gì mới
git log origin/main

# Merge thủ công nếu muốn
git merge origin/main
```

### Xem thay đổi trước khi pull
```bash
# Fetch trước
git fetch origin

# Xem diff giữa local và remote
git diff main origin/main

# Xem commit mới trên remote
git log main..origin/main

# Xem chi tiết thay đổi
git log -p main..origin/main
```

---

## Xử lý các tình huống đặc biệt

### Tình huống 1: Quên stash/commit trước khi pull
```
error: Your local changes to the following files would be overwritten by merge:
    file1.js
Please commit your changes or stash them before you merge.
```

**Giải pháp:**
```bash
# Option 1: Stash
git stash
git pull origin main
git stash pop

# Option 2: Commit
git add .
git commit -m "WIP: Save work before pull"
git pull origin main
```

### Tình huống 2: Conflict phức tạp, muốn hủy merge
```bash
# Hủy merge đang thực hiện
git merge --abort

# Quay về trạng thái trước khi pull
git reset --hard HEAD
```

### Tình huống 3: Pull nhầm code, muốn quay lại
```bash
# Xem lịch sử để tìm commit cần quay lại
git log --oneline

# Quay lại commit cụ thể
git reset --hard <commit-hash>

# Ví dụ: git reset --hard abc1234
```

### Tình huống 4: Remote có force push, local bị lỗi
```bash
# Fetch thông tin mới
git fetch origin

# Reset về trạng thái của remote
git reset --hard origin/main

# CẨN THẬN: Lệnh này sẽ XÓA tất cả thay đổi local!
```

### Tình huống 5: Muốn xem code mới trước khi merge
```bash
# Fetch về trước
git fetch origin

# Checkout sang remote branch để xem
git checkout origin/main

# Xem code, test, etc.

# Quay lại main
git checkout main

# Pull nếu oke
git pull origin main
```

---

## So sánh Git Pull vs Git Fetch

| Đặc điểm | `git fetch` | `git pull` |
|----------|-------------|------------|
| Tải code từ remote | ✅ Có | ✅ Có |
| Merge vào local | ❌ Không | ✅ Có |
| An toàn | ✅ Rất an toàn | ⚠️ Có thể gây conflict |
| Khi nào dùng | Khi muốn xem code trước | Khi muốn cập nhật ngay |

**Khuyến nghị:**
```bash
# Cách an toàn hơn:
git fetch origin        # Tải về trước
git diff main origin/main  # Xem thay đổi
git merge origin/main   # Merge khi đã sẵn sàng

# Cách nhanh hơn:
git pull origin main    # Tải và merge luôn
```

---

## Checklist khi Pull Code

- [ ] Đã commit hoặc stash thay đổi hiện tại
- [ ] Đang ở đúng branch (main)
- [ ] Kiểm tra connection với remote: `git remote -v`
- [ ] Pull code: `git pull origin main`
- [ ] Resolve conflict nếu có
- [ ] Test code sau khi pull
- [ ] Xác nhận code đã cập nhật: `git log`
- [ ] Thông báo team nếu có conflict hoặc vấn đề

---

## Tips & Best Practices

### ✅ Nên làm:
- Pull code thường xuyên (mỗi 1-2 giờ)
- Pull trước khi bắt đầu làm việc mới
- Pull trước khi push code
- Commit hoặc stash thay đổi trước khi pull
- Test kỹ code sau khi pull

### ❌ Không nên:
- Làm việc nhiều ngày không pull code
- Pull khi có nhiều thay đổi chưa commit
- Bỏ qua conflict resolution
- Force push sau khi có conflict
- Panic khi gặp conflict (bình tĩnh resolve)

### 💡 Thủ thuật:
```bash
# Tạo alias để pull nhanh hơn
git config --global alias.pl "pull origin main"
# Giờ chỉ cần: git pl

# Auto stash khi pull
git config --global pull.rebase true
git config --global rebase.autoStash true
```
