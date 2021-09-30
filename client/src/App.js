import { useEffect, useState } from 'react';
import 'antd/dist/antd.css'
import './App.css';
import { Layout, Menu } from 'antd'
import { AppstoreAddOutlined, AreaChartOutlined, InfoCircleOutlined } from '@ant-design/icons';
const { Header, Footer, Content, Sider } = Layout;
const Slider = Sider;
const { SubMenu } = Menu;



function App() {
  var [collapsed, setCollapsed] = useState(false);
  var [page, setPage] = useState("1")

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Slider collapsible collapsed={collapsed} onCollapse={(collapsed, type) => setCollapsed(collapsed)}>
        <div className="block" />
        <Menu theme="dark" defaultActiveFirst mode="inline" onClick={(info) => { setPage(info.key) }}>
          <Menu.Item key="1" icon={<InfoCircleOutlined />} >按键统计</Menu.Item>
          <Menu.Item key="2" icon={<AreaChartOutlined />}>分析</Menu.Item>
        </Menu>
      </Slider>
      <Layout className="site-layout">
        <Header className="site-layout-background" style={{ padding: 0 }} />
        <Content style={{ margin: '0 16px' }}>
          <p>Title</p>
          <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
            123321
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>333</Footer>
      </Layout>
    </Layout >
  );
}

export default App;
