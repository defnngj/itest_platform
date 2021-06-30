describe('用例管理', () => {
  it('搜索用例', () => {
    cy.visit('/#/cases')
    cy.get('[cy-data=team]', { timeout: 3000}).click()
    cy.get('[cy-data=team-list]', { timeout: 3000}).first().click()
    cy.get('[cy-data=search-keyword]', { timeout: 3000 }).first().type('用例名称')
    cy.get('[cy-data=search-button]', { timeout: 3000 }).first().click()  // 搜索
  });  
  it('列表翻页', () => {
    cy.visit('/#/cases')
    cy.wait(1000)
    cy.get('button.btn-next', { timeout: 3000 }).click() // 点击下一页
    cy.get('button.btn-prev', { timeout: 3000 }).click() // 点击上一页
    cy.get('ul.el-pager > li.number', { timeout: 3000 }).eq(1).click() // 点击第2页
  });
  it('创建用例-手动创建', () => {
    cy.visit('/#/cases')
    cy.get('[cy-data=create-case]', { timeout: 3000 }).click()
    cy.get('[cy-data=manual]', { timeout: 3000 }).click()
    cy.wait(1000)
    cy.get('[cy-data=case-name]').type('首页接口压测 - 用例')
    cy.get('[cy-data=case-desc]').type('用例备注信息')
    cy.get('[cy-data=team]').click() // 团队
    cy.get('[cy-data=team-list]', { timeout: 3000}).first().click()
    cy.get('[cy-data=env]').click() // 环境
    cy.get('[cy-data=env-list]', { timeout: 3000}).first().click()
    cy.get('[cy-data=monitor]').click() // 监控分组
    cy.get('[cy-data=monitor-list]', { timeout: 3000}).first().click()
    cy.get('[cy-data=email]').click() // 邮件分组
    cy.get('[cy-data=email-list]', { timeout: 3000}).first().click()
    // JMeter 参数配置
    cy.get('[cy-data=slave-count] > span').eq(1).click()
    cy.get('[cy-data=target-concurrency] > span').first().click()
    cy.get('[cy-data=ramp-up-time] > span').eq(1).click()
    cy.get('[cy-data=ramp-up-steps-count] > span').eq(1).click()
    cy.get('[cy-data=hold-target-rate-time] > div > input').clear().type('100')
    // 保存用例
    cy.get('[cy-data=save-button]').click()
  });
  it('创建用例->自动创建->流量日志', () => {
    cy.visit('/#/cases')
    cy.get('[cy-data=create-case]', { timeout: 3000 }).click()
    cy.get('[cy-data=automatic]', { timeout: 3000 }).click()
    cy.wait(1000)
    cy.get('[cy-data=create-flowlog]').click()
    cy.get('[cy-data=flowlog-name]').type('创建流量日志')
    cy.get('[cy-data=flowlog-desc]').type('流量日志描述')
    cy.get('[cy-data=url-path]').type('/api')
    cy.get('[cy-data=protocol]').click()
    cy.get('[cy-data=protocol-list]', { timeout: 3000 }).first().click()
    cy.get('[cy-data=method]').click()
    cy.get('[cy-data=method-list]', { timeout: 3000 }).first().click()
    cy.get('[cy-data=start-time]').clear().type('2021-03-01 16:02:50')
    cy.get('[cy-data=end-time]').clear().type('2021-04-01 16:02:50')
    // 查看日志
    cy.get('[cy-data=show-log]').click()
    cy.contains('查看流量日志')
  });
  it('创建用例->自动创建->创建用例', () => {
    cy.visit('/#/cases')
    cy.get('[cy-data=create-case]', { timeout: 3000 }).click()
    cy.get('[cy-data=automatic]', { timeout: 3000 }).click()
    cy.wait(1000)
    // 选择流量日志
    cy.get('[cy-data=flowlog]').click()
    cy.get('[cy-data=flowlog-list]', { timeout: 3000 }).first().click()
    cy.get('[cy-data=generate-case]').click()
    // 创建用例
    cy.get('[cy-data=team]').click() // 团队
    cy.get('[cy-data=team-list]', { timeout: 3000}).first().click()
    cy.get('[cy-data=env]').click() // 环境
    cy.get('[cy-data=env-list]', { timeout: 3000}).first().click()
    cy.get('[cy-data=host]').type('t11.klook.io')
    cy.get('[cy-data=assertion]').clear().type('success')
    // 保存用例
    cy.get('[cy-data=save-case]').click()
  });
  it('执行用例', () => {
    cy.visit('/#/cases')
    cy.get('[cy-data=run-case]', { timeout: 3000}).first().click({ force: true })
  });
  it('删除用例', () => {
    cy.visit('/#/cases')
    cy.get('[cy-data=delete-case]', { timeout: 3000}).first().click({ force: true })
    cy.get('.el-message-box__btns > button', { timeout: 3000 }).eq(1).click()  //确定删除
  });
  it('查看报告', () => {
    cy.visit('/#/cases')
    cy.get('[cy-data=link-to-report]', { timeout: 3000}).first().click({ force: true })
    cy.contains('报告管理')
  });
})
