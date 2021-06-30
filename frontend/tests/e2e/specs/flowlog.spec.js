describe('项目管理', () => {
  it('搜索流量日志', () => {
    cy.visit('/#/flowlog')
    cy.get('div.el-input > input[type=text]', { timeout: 3000 }).first().type('流量日志')
    cy.get('button.el-button--primary', { timeout: 3000 }).first().click()  // 搜索
  });
  it('列表翻页', () => {
    cy.visit('/#/flowlog')
    cy.wait(2000)
    cy.get('ul.el-pager > li.number', { timeout: 3000 }).eq(1).click() // 点击第2页
    cy.get('button.btn-next', { timeout: 3000 }).click() // 点击下一页
    cy.get('button.btn-prev', { timeout: 3000 }).click() // 点击上一页
  });
  it('添加流量日志', () => {
    cy.visit('/#/flowlog')
    cy.get('span.span-left:nth-child(3) > button.el-button', { timeout: 3000 }).click()
    cy.get('[cy-data=name]', { timeout: 3000 }).type('流量日志名称')
    cy.get('[cy-data=desc]', { timeout: 3000 }).type('流量日志描述')
    cy.get('[cy-data=url-path]', { timeout: 3000 }).type('/api/v1/home')
    cy.get('[cy-data=protocol]', { timeout: 3000 }).click()
    cy.get('[cy-data=protocol-list]').eq(0).click()
    cy.get('[cy-data=method]', { timeout: 3000 }).click()
    cy.get('[cy-data=method-list]').eq(0).click()
    cy.get('[cy-data=start-time]').clear().type("2021-03-22 12:00:00")
    cy.get('[cy-data=end-time]').clear().type("2021-03-22 18:00:00")
    cy.get('[cy-data=save-button]').click() //保存流量日志
  });
  it('编辑流量日志', () => {
    cy.visit('/#/flowlog')
    cy.wait(2000)
    cy.get('[cy-data=edit-flowlog]', { timeout: 3000 }).first().click({ force: true })  // 编辑流量日志
    cy.get('[cy-data=name]', { timeout: 3000 }).clear().type('更新流量日志名称')
    cy.get('[cy-data=desc]', { timeout: 3000 }).clear().type('更新流量日志描述')
    cy.get('[cy-data=url-path]', { timeout: 3000 }).clear().type('/api/v1/flowlog')
    cy.get('[cy-data=protocol]', { timeout: 3000 }).click()
    cy.get('[cy-data=protocol-list]').eq(1).click()
    cy.get('[cy-data=method]', { timeout: 3000 }).click()
    cy.get('[cy-data=method-list]').eq(0).click()
    cy.get('[cy-data=start-time]').clear().type("2021-03-22 12:00:00")
    cy.get('[cy-data=end-time]').clear().type("2021-03-22 18:00:00")
    cy.get('[cy-data=save-button]').click() // 保存流量日志
  });
  it('删除流量日志', () => {
    cy.visit('/#/flowlog')
    cy.wait(1000)
    cy.get('[cy-data=delete-flowlog]', { timeout: 3000 }).first().click({ force: true })  // 删除流量日志
    cy.get('.el-message-box__btns > button', { timeout: 3000 }).eq(1).click()  //确定删除
  });
  it('生成日志', () => {
    cy.visit('/#/flowlog')
    cy.wait(1000)
    cy.get('[cy-data=generate-log]', { timeout: 3000 }).first().click({ force: true })  // 生成日志
  });
  it('日志预览', () => {
    cy.visit('/#/flowlog')
    cy.wait(1000)
    cy.get('[cy-data=show-log]', { timeout: 3000 }).first().click({ force: true })  // 日志预览
    cy.contains('查看流量日志')
    cy.contains('Lines')
    cy.contains('Bytes')
    cy.get('button.el-dialog__headerbtn').first().click()
  });
})