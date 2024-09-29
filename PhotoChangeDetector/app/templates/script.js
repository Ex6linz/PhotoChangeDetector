document.getElementById('file_upload').addEventListener('change', function () {
  const fileName = this.value.split('\\').pop();
  document.getElementById('file_name').textContent = fileName ? `Selected file: ${fileName}` : '';
});