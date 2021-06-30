describe('邮件分组', () => {
    it('搜索邮件分组', () => {
      cy.visit('/#/email')
      cy.get('[cy-data=search-email]', { timeout: 3000 }).first().type('邮件分组')
      cy.get('[cy-data=search-button]', { timeout: 3000 }).first().click()  // 搜索
    });
    it('添加邮件分组', () => {
      cy.visit('/#/email')
      cy.get('[cy-data=create-button]', { timeout: 3000 }).click()
      cy.get('[cy-data=name]', { timeout: 3000 }).type('邮件分组名称')
      cy.get('[cy-data=select-email]', { timeout: 3000 }).click()
      cy.get('[cy-data=email-list]').eq(0).click()
      cy.get('[cy-data=save-button]').click() //保存流量日志
    });
    it('编辑邮件分组', () => {
      cy.visit('/#/email')
      cy.wait(2000)
      cy.get('[cy-data=edit-email]', { timeout: 3000 }).eq(-1).click()
      cy.get('[cy-data=name]', { timeout: 3000 }).type('更新邮件分组名称')
      cy.get('[cy-data=select-email]', { timeout: 3000 }).click()
      cy.get('[cy-data=email-list]').eq(0).click()
      cy.get('[cy-data=save-button]').click() //保存流量日志
    });
    it('删除邮件分组', () => {
      cy.visit('/#/email')
      cy.wait(2000)
      cy.get('[cy-data=delete-email]', { timeout: 3000 }).first().click({ force: true })  // 删除邮件分组
      cy.get('.el-message-box__btns > button', { timeout: 3000 }).eq(1).click()  //确定删除
    });
  })