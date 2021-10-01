import React, { useState } from 'react';
import 'antd/dist/antd.css'
import './App.css';
import { Layout, Menu } from 'antd'
import { AreaChartOutlined, InfoCircleOutlined, SearchOutlined } from '@ant-design/icons';
import { PageSearch, PageStatistics } from './pages/pages'

const { Header, Footer, Content, Sider } = Layout;
const Slider = Sider;


var Pages = {
  Search: "Search",
  Statistics: "Statistics",
  Analysis: "Analysis"
}

function Page(props) {
  switch (props.page) {
    case Pages.Statistics:
      return <PageStatistics />
    case Pages.Analysis:
      console.log(222)
      return <p>Analysis</p>;

    case Pages.Search:
    default:
      return <PageSearch />
  }
}


function App() {
  var [collapsed, setCollapsed] = useState(false);
  var [page, setPage] = useState(Pages.Search)
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Slider collapsible collapsed={collapsed} onCollapse={(collapsed, type) => setCollapsed(collapsed)}>
        <div className="block" />
        <Menu theme="dark" mode="inline" onClick={(info) => { setPage(info.key); }}>
          <Menu.Item key={Pages.Search} icon={<SearchOutlined />}>搜索码表</Menu.Item>
          <Menu.Item key={Pages.Statistics} icon={<InfoCircleOutlined />} >按键统计</Menu.Item>
          <Menu.Item key={Pages.Analysis} icon={<AreaChartOutlined />}>分析</Menu.Item>
        </Menu>
      </Slider>
      <Layout className="site-layout">
        <Header className="site-layout-background" style={{ padding: 0 }} />
        <Content style={{ margin: '0 16px' }}>
          <p>Title</p>
          <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
            <Page page={page}></Page>
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>333</Footer>
      </Layout>
    </Layout >
  );
}

export default App;
