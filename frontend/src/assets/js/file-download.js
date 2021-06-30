import { jsPDF } from 'jspdf'

export function exportPdf(name, canvasList) {

  const pdf = new jsPDF('', 'pt', 'a4')

  // 当前页面的当前高度
  let currentHeight = 0
  for (const canvas of canvasList) {
    if (canvas) {

      const contentWidth = canvas.width
      const contentHeight = canvas.height

      // a4纸的尺寸[595.28,841.89]
      const a4Width = 592.28
      const a4Height = 841.89

      // html页面生成的canvas在pdf中图片的宽高
      const imgWidth = a4Width
      const imgHeight = a4Width / contentWidth * contentHeight

      const pageData = canvas.toDataURL('image/jpeg', 1.0)

      // 当前图片的剩余高度
      let leftHeight = imgHeight;

      // 当前页面的剩余高度
      const blankHeight = a4Height - currentHeight

      if (leftHeight > blankHeight) {
        // 页面偏移
        let position = 0;
        while (leftHeight > 0) {
          // 本次添加占用的高度
          const occupation = a4Height - currentHeight;
          pdf.addImage(pageData, 'JPEG', 0, position + currentHeight, imgWidth, imgHeight)
          currentHeight = leftHeight
          leftHeight -= occupation
          position -= occupation
          // 避免添加空白页
          if (leftHeight > 0) {
            pdf.addPage()
            currentHeight = 0
          }
        }
      } else {
        pdf.addImage(pageData, 'JPEG', 0, currentHeight, imgWidth, imgHeight)
        currentHeight += imgHeight
      }
    }
  }

  pdf.save(name.replace(' ', '_') + '.pdf');
}

export function downloadFile(name, content, options) {
  const blob = new Blob([content], options);
  if ('download' in document.createElement('a')) {
    // 非IE下载,chrome/firefox
    const aTag = document.createElement('a');
    aTag.download = name;
    aTag.href = URL.createObjectURL(blob);
    aTag.click();
    URL.revokeObjectURL(aTag.href)
  } else {
    // IE10+下载
    navigator.msSaveBlob(blob, this.filename)
  }
}
