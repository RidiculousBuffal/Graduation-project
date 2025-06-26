import React, { useState, useEffect } from 'react';
import { Select, message } from 'antd';
import { getEngineers } from '@/api/userapi.ts';
import type { userType } from '@/store/user/types.ts';

interface EngineerSelectorProps {
    value?: string;
    onChange?: (value: string) => void;
    placeholder?: string;
    disabled?: boolean;
}

const EngineerSelector: React.FC<EngineerSelectorProps> = ({
                                                               value,
                                                               onChange,
                                                               placeholder = "请选择执行工程师",
                                                               disabled = false
                                                           }) => {
    const [engineers, setEngineers] = useState<userType[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadEngineers().then(r => r);
    }, []);

    const loadEngineers = async () => {
        setLoading(true);
        try {
            const result = await getEngineers();
            if (result) {
                setEngineers(result);
            }
        } catch (error) {
            console.error('加载工程师列表失败:', error);
            message.error('加载工程师列表失败');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Select
            value={value}
            onChange={onChange}
            placeholder={placeholder}
            disabled={disabled}
            loading={loading}
            allowClear
            showSearch
            optionFilterProp="children"
            style={{ width: '100%' }}
        >
            {engineers.map(engineer => (
                <Select.Option key={engineer.user_id} value={engineer.user_id}>
                    {engineer.username} ({engineer.email?engineer.email:"未设置邮箱"})
                </Select.Option>
            ))}
        </Select>
    );
};

export default EngineerSelector;