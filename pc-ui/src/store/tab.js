export default{
    state:{
        isCollapse:false,//导航栏是否折叠
        tabList: [
            {
                path: '/',
                name: 'home',
                label: '首页',
                icon: 's-home',
                url: 'Home/Home'
            }
        ]
    },
    mutations:{
        // 修改导航栏展开和收起的方法
        CollapseMenu(state){
            state.isCollapse=!state.isCollapse
        },
        // 更新面包屑数据
        SelectMenu(state, item){
            const index = state.tabList.findIndex(val => val.name === item.name)
            if(index === -1){
                state.tabList.push(item)
            }
        },
        // 删除tag
        closeTag(state, item){
            const index = state.tabList.findIndex(val => val.name === item.name)
            state.tabList.splice(index, 1)
        }
    }
}