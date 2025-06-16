import React, {useState} from 'react';
import {Input, AutoComplete, Button, Space, Form} from 'antd';
import {SearchOutlined, ReloadOutlined, UploadOutlined} from '@ant-design/icons';
import {AircraftListService} from "../../../services/AircraftListService.ts";
import {useAircraftStore} from "../../../store/aircraft/aircraftStore.ts";
import './SearchBar.css';

interface SearchBarProps {
    onSearch: (values: { image_name?: string; aircraft_id?: string; aircraft_name?: string }) => void;
    onReset: () => void;
    loading?: boolean;
    onCreate:()=>void;
}

const SearchBar: React.FC<SearchBarProps> = ({onSearch, onReset, loading = false,onCreate}) => {
    const [form] = Form.useForm();
    const [aircraftOptions, setAircraftOptions] = useState<Array<{ value: string; label: string }>>([]);
    const [searchingAircraft, setSearchingAircraft] = useState(false);

    const handleSearch = () => {
        const values = form.getFieldsValue();
        onSearch(values);
    };

    const handleReset = () => {
        form.resetFields();
        setAircraftOptions([]);
        onReset();
    };

    const handleAircraftSearch = async (searchText: string) => {
        if (!searchText || searchText.length < 2) {
            setAircraftOptions([]);
            return;
        }

        setSearchingAircraft(true);
        try {
            // 使用 AircraftListService 搜索飞机
            await AircraftListService.getAircraftList({
                aircraft_name: searchText,
                age: null,
                type_name: null,
                description: null
            });

            // 从 store 中获取搜索结果
            const {aircrafts} = useAircraftStore.getState();

            const options = aircrafts.map((aircraft: any) => ({
                value: aircraft.aircraft_name,
                label: aircraft.aircraft_name,
                data: aircraft
            }));

            setAircraftOptions(options);
        } catch (error) {
            console.error('搜索飞机失败:', error);
            setAircraftOptions([]);
        } finally {
            setSearchingAircraft(false);
        }
    };

    return (
        <div className="search-bar">
            <Form form={form} layout="inline" className="search-form">
                <div className="search-inputs">
                    <Form.Item name="image_name" label="图片名称" className="search-item">
                        <Input
                            placeholder="请输入图片名称"
                            allowClear
                            onPressEnter={handleSearch}
                        />
                    </Form.Item>

                    <Form.Item name="aircraft_name" label="飞机名称" className="search-item">
                        <AutoComplete
                            placeholder="请输入飞机名称"
                            options={aircraftOptions}
                            onSearch={handleAircraftSearch}
                            notFoundContent={searchingAircraft ? '搜索中...' : '暂无数据'}
                            allowClear
                            filterOption={false}
                        />
                    </Form.Item>

                    <Form.Item className="search-actions">
                        <Space>
                            <Button
                                type="primary"
                                icon={<SearchOutlined/>}
                                onClick={handleSearch}
                                loading={loading}
                            >
                                搜索
                            </Button>
                            <Button
                                icon={<ReloadOutlined/>}
                                onClick={handleReset}
                            >
                                重置
                            </Button>
                        </Space>
                    </Form.Item>
                </div>

                <div className="upload-section">
                    <Button
                        type="primary"
                        icon={<UploadOutlined/>}
                        onClick={onCreate}
                        className="upload-button"
                    >
                        上传底图
                    </Button>
                </div>
            </Form>
        </div>
    );
};

export default SearchBar;