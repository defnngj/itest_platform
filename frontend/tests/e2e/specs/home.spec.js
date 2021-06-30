// https://docs.cypress.io/api/introduction/api.html

describe('测试首页', () => {
  it('测试排期列表', () => {
    cy.visit('/')
    cy.get('tbody > tr > td > div', { timeout: 3000 }).first()
      .should('contain', 'hetel产线压测') // assertion
  });
  it('测试热点地图', () => {
    cy.visit('/')
    // 检查文本
    cy.contains('Less')
    cy.contains('More')

    cy.contains('Mon')
    cy.contains('Wed')
    cy.contains('Fri')
  })
})
