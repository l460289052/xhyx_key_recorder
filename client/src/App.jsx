import React, { useEffect, useState } from 'react';
import 'antd/dist/antd.css'
import './App.css';
import { Button, Layout, Menu, Space, Switch } from 'antd'
import { AreaChartOutlined, InfoCircleOutlined, SearchOutlined } from '@ant-design/icons';
import { PageSearch, PageStatistics } from './pages/pages'
import axios from 'axios';

const { Header, Footer, Content, Sider } = Layout;
const Slider = Sider;


var Pages = {
  Search: "Search",
  Statistics: "Statistics",
  Analysis: "Analysis"
}

var ShownName = {
  Search: "搜索码表",
  Statistics: "按键统计",
  Analysis: "分析"
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
  var [running, setRunning] = useState(false)
  var [page, setPage] = useState(Pages.Search)

  useEffect(() => axios.get("/api/get_hook_state")
    .then(rep => setRunning(rep.data.running))
    , [])

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Slider collapsible collapsed={collapsed} onCollapse={(collapsed, type) => setCollapsed(collapsed)}>
        <div className="block">
        </div>
        <div style={{ textAlign: 'center' }}>
          <p style={{ display: 'inline', color: 'white' }}>运行状态</p>
          <Button type="primary" size="small" danger={!running}
            onClick={e => {
              axios.post("/api/set_hook_state", {}, { params: { running: !running } })
                .then(rep => axios.get("/api/get_hook_state")
                  .then(rep => setRunning(rep.data.running)))
            }}
          >
            {running ? "运行中" : "未运行"}
          </Button>

        </div>
        <Menu theme="dark" mode="inline" onClick={(info) => { setPage(info.key); }}>
          <Menu.Item key={Pages.Search} icon={<SearchOutlined />}>{ShownName[Pages.Search]}</Menu.Item>
          <Menu.Item key={Pages.Statistics} icon={<InfoCircleOutlined />} >{ShownName[Pages.Statistics]}</Menu.Item>
          <Menu.Item key={Pages.Analysis} icon={<AreaChartOutlined />}>{ShownName[Pages.Analysis]}</Menu.Item>
        </Menu>
      </Slider>
      <Layout className="site-layout">
        <Header className="site-layout-background" style={{ padding: 0 }} />
        <Content style={{ margin: '0 16px' }}>
          <p>{ShownName[page]}</p>
          <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
            <Page page={page}></Page>
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>By 其无能名</Footer>
      </Layout>
    </Layout >
  );
}

export default App;
