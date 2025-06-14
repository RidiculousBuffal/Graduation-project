import React, {useEffect} from 'react';
import {Modal, Form, Input, message} from 'antd';
import {TerminalService} from "../../services/TerminalService.ts";
import type {terminalType} from "../../store/terminal/types.ts";


interface TerminalEditModalProps {
    visible: boolean;
    terminal: terminalType | null;
    onCancel: () => void;
    onSuccess: () => void;
}

const TerminalEditModal: React.FC<TerminalEditModalProps> = ({
                                                                 visible,
                                                                 terminal,
                                                                 onCancel,
                                                                 onSuccess
                                                             }) => {
    const [form] = Form.useForm();
    const [loading, setLoading] = React.useState(false);

    useEffect(() => {
        if (visible && terminal) {
            form.setFieldsValue({
                terminal_name: terminal.terminal_name,
                description: terminal.description || ''
            });
        }
    }, [visible, terminal, form]);

    const handleSubmit = async () => {
        if (!terminal) return;

        try {
            const values = await form.validateFields();
            setLoading(true);

            await TerminalService.updateTerminal({
                terminal_id: terminal.terminal_id,
                terminal_name: values.terminal_name,
                description: values.description || null
            });
            onSuccess();
        } catch (error) {
            message.error('更新失败，请重试');
        } finally {
            setLoading(false);
        }
    };

    const handleCancel = () => {
        form.resetFields();
        onCancel();
    };

    return (
        <Modal
            title="编辑航站楼"
            open={visible}
            onOk={handleSubmit}
            onCancel={handleCancel}
            confirmLoading={loading}
            okText="保存"
            cancelText="取消"
            destroyOnClose
        >
            <Form
                form={form}
                layout="vertical"
                autoComplete="off"
            >
                <Form.Item
                    label="航站楼名称"
                    name="terminal_name"
                    rules={[
                        {required: true, message: '请输入航站楼名称'},
                        {min: 2, message: '航站楼名称至少2个字符'},
                        {max: 50, message: '航站楼名称不能超过50个字符'}
                    ]}
                >
                    <Input placeholder="请输入航站楼名称"/>
                </Form.Item>

                <Form.Item
                    label="描述"
                    name="description"
                    rules={[
                        {max: 1000, message: '描述不能超过1000个字符'}
                    ]}
                >
                    <Input.TextArea
                        rows={4}
                        placeholder="请输入航站楼描述（支持Markdown格式）"
                    />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default TerminalEditModal;