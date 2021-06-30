describe('报告管理', () => {
  it('搜索报告', () => {
    cy.visit('/#/report')
    cy.get('[cy-data=search-project]', { timeout: 3000 }).first().type('项目名称')
    cy.get('[cy-data=search-button]', { timeout: 3000 }).first().click()  // 搜索
  });

})
