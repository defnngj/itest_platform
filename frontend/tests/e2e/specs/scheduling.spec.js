
describe('日程安排', () => {
  it('切换月份', () => {
    cy.visit('#/scheduling')
    cy.get('button[aria-label=prev]', { timeout: 3000 }).click()
    cy.get('h2.fc-toolbar-title', { timeout: 5000 }).should('contain', '2021年2月') // assertion
    cy.get('button[aria-label=next]', { timeout: 3000 }).click()
    cy.get('h2.fc-toolbar-title').should('contain', '2021年3月') // assertion
  });
  it('切换日程/月/周', () => {
    cy.visit('#/scheduling')
    cy.get('button.fc-listMonth-button').click()  // 日程
    cy.wait(1000)
    cy.get('button.fc-dayGridMonth-button').click()  // 月
    cy.get('div.fc-daygrid-day-frame').should('have.length', 42)  // 检查日历
    cy.wait(1000)
    cy.get('button.fc-timeGridWeek-button').click()  // 周
  });
  it('添加任务', () => {
    cy.visit('#/scheduling')
    cy.get('div.fc-daygrid-day-frame').first().click()
    cy.get('[cy-data=task-name]', { timeout: 3000 }).type('event')
    cy.get('[cy-data=team]', { timeout: 3000 }).click()
    cy.get('[cy-data=team-list]').eq(0).click()
    cy.get('[cy-data=end-time] > input').clear().type("18:00")
    cy.get('[cy-data=start-time] > input').clear().type("14:00")
    cy.get('[cy-data=save-task]').click()
  })
  it('更新任务', () => {
    cy.visit('#/scheduling')
    cy.get('div.fc-event-time').first().click()
    cy.get('[cy-data=task-name]', { timeout: 3000 }).eq(0).clear().type('new event')
    cy.get('[cy-data=team]', { timeout: 3000 }).click()
    cy.get('[cy-data=team-list]').eq(0).click()
    cy.get('[cy-data=end-time] > input').clear().type("12:00")
    cy.get('[cy-data=start-time] > input').clear().type("10:00")
    cy.get('[cy-data=save-task]').click()
  })
  it('删除任务', () => {
    cy.visit('#/scheduling')
    cy.get('div.fc-event-time').first().click()
    cy.get('[cy-data=delete-task]').click()
    cy.get('.el-message-box__btns > button', { timeout: 3000 }).eq(1).click()
  })

})
