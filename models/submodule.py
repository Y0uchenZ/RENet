import torch
import torch.nn as nn
import torch.utils.data
import torch.nn.functional as F
import numpy as np
# from mmcv.ops import DeformConv2dPack as DCN


# 2d conv+BN
def convbn(in_channels, out_channels, kernel_size, stride, pad, dilation=1):
    return nn.Sequential(nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride,
                                   padding=dilation if dilation > 1 else pad, dilation=dilation, bias=False),
                         nn.BatchNorm2d(out_channels))


# 2d convDeform+BN
# def convDeform_bn(in_channels, out_channels, kernel_size, stride, pad, deform_groups=1):
#     return nn.Sequential(DCN(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=pad,
#                              deform_groups=deform_groups),
#                          nn.BatchNorm2d(out_channels))


# 2d convTrans+BN
def convTrans_bn(in_channels, out_channels, kernel_size, stride, pad, output_pad):
    return nn.Sequential(nn.ConvTranspose2d(in_channels, out_channels, kernel_size, padding=pad,
                                            output_padding=output_pad, stride=stride, bias=False),
                         nn.BatchNorm2d(out_channels))


# 2d group conv+BN
def convbn_group(in_channels, out_channels, groups, kernel_size, stride, pad, dilation):
    return nn.Sequential(nn.Conv2d(in_channels, out_channels, groups=groups, kernel_size=kernel_size, stride=stride,
                                   padding=dilation if dilation > 1 else pad, dilation=dilation, bias=False),
                         nn.BatchNorm2d(out_channels))


# 3d conv+BN
def convbn_3d(in_channels, out_channels, kernel_size, stride, pad):
    return nn.Sequential(nn.Conv3d(in_channels, out_channels, kernel_size=kernel_size, padding=pad,
                                   stride=stride, bias=False),
                         nn.BatchNorm3d(out_channels))


# 3d convTrans+BN
def convTrans_3d_bn(in_channels, out_channels, kernel_size, stride, pad, output_pad):
    return nn.Sequential(nn.ConvTranspose3d(in_channels, out_channels, kernel_size, padding=pad,
                                            output_padding=output_pad, stride=stride, bias=False),
                         nn.BatchNorm3d(out_channels))


# 3d group conv+BN
def convbn_3d_group(in_channels, out_channels, groups, kernel_size, stride, pad):
    return nn.Sequential(nn.Conv3d(in_channels, out_channels, groups=groups, kernel_size=kernel_size, stride=stride,
                                   padding=pad, bias=False),
                         nn.BatchNorm3d(out_channels))


# 2d conv+GN
def convgn(in_channels, out_channels, kernel_size, stride, pad, dilation):
    return nn.Sequential(nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride,
                                   padding=dilation if dilation > 1 else pad, dilation=dilation, bias=False),
                         nn.GroupNorm(4, out_channels))


# 2d group conv+GN
def convgn_group(in_channels, out_channels, groups, kernel_size, stride, pad, dilation):
    return nn.Sequential(nn.Conv2d(in_channels, out_channels, groups=groups, kernel_size=kernel_size, stride=stride,
                                   padding=dilation if dilation > 1 else pad, dilation=dilation, bias=False),
                         nn.GroupNorm(4, out_channels))


# 3d conv+GN
def convgn_3d(in_channels, out_channels, kernel_size, stride, pad):
    return nn.Sequential(nn.Conv3d(in_channels, out_channels, kernel_size=kernel_size, stride=stride,
                                   padding=pad, bias=False),
                         nn.GroupNorm(4, out_channels))


# 3d group conv+GN
def convgn_3d_group(in_channels, out_channels, groups, kernel_size, stride, pad):
    return nn.Sequential(nn.Conv3d(in_channels, out_channels, groups=groups, kernel_size=kernel_size, stride=stride,
                                   padding=pad, bias=False),
                         nn.GroupNorm(4, out_channels))


# 3d conv+BN，kernel size=1*k*k
def convbn_3d_1kk(in_channels, out_channels, kernel_size, stride, pad):
    return nn.Sequential(
        nn.Conv3d(in_channels, out_channels, kernel_size=(1, kernel_size, kernel_size), stride=(1, stride, stride),
                  padding=(0, pad, pad), bias=False),
        nn.BatchNorm3d(out_channels))


# 3 groups 3d conv(kernel size: k*1*1, 1*k*1, 1*1*k)+BN
def convbn_3d_new(in_channels, out_channels, kernel_size, stride, pad):
    return nn.Sequential(nn.Conv3d(in_channels, out_channels, kernel_size=(kernel_size, 1, 1), stride=(stride, 1, 1),
                                   padding=(pad, 0, 0), bias=False),
                         nn.Conv3d(out_channels, out_channels, kernel_size=(1, kernel_size, 1), stride=(1, stride, 1),
                                   padding=(0, pad, 0), bias=False),
                         nn.Conv3d(out_channels, out_channels, kernel_size=(1, 1, kernel_size), stride=(1, 1, stride),
                                   padding=(0, 0, pad), bias=False),
                         nn.BatchNorm3d(out_channels))


# 3 groups 3d conv(kernel size: k*1*1, 1*k*1, 1*1*k)
def conv_3d_new(in_channels, out_channels, kernel_size, stride, pad):
    return nn.Sequential(nn.Conv3d(in_channels, out_channels, kernel_size=(kernel_size, 1, 1), stride=(stride, 1, 1),
                                   padding=(pad, 0, 0), bias=False),
                         nn.Conv3d(out_channels, out_channels, kernel_size=(1, kernel_size, 1), stride=(1, stride, 1),
                                   padding=(0, pad, 0), bias=False),
                         nn.Conv3d(out_channels, out_channels, kernel_size=(1, 1, kernel_size), stride=(1, 1, stride),
                                   padding=(0, 0, pad), bias=False))


# 3 groups 3d convTrans(kernel size: k*1*1, 1*k*1, 1*1*k)
def convTrans_3d_new(in_channels, out_channels, kernel_size, pad, output_pad, stride):
    return nn.Sequential(
        nn.ConvTranspose3d(in_channels, out_channels, kernel_size=(kernel_size, 1, 1), stride=(stride, 1, 1),
                           padding=(pad, 0, 0), output_padding=(output_pad, 0, 0), bias=False),
        nn.ConvTranspose3d(out_channels, out_channels, kernel_size=(1, kernel_size, 1), stride=(1, stride, 1),
                           padding=(0, pad, 0), output_padding=(0, output_pad, 0), bias=False),
        nn.ConvTranspose3d(out_channels, out_channels, kernel_size=(1, 1, kernel_size), stride=(1, 1, stride),
                           padding=(0, 0, pad), output_padding=(0, 0, output_pad), bias=False))


# 2 groups 3d conv(first DW)+BN
def convbn_3d_dw(in_channels, out_channels, kernel_size, stride, pad):
    return nn.Sequential(nn.Conv3d(in_channels, in_channels, kernel_size=kernel_size, stride=stride,
                                   padding=pad, bias=False, groups=in_channels),
                         nn.Conv3d(in_channels, out_channels, kernel_size=1),
                         nn.BatchNorm3d(out_channels))


# 2 groups 3d conv(first DW)
def conv_3d_dw(in_channels, out_channels, kernel_size, stride, pad):
    return nn.Sequential(nn.Conv3d(in_channels, in_channels, kernel_size=kernel_size, stride=stride,
                                   padding=pad, bias=False, groups=in_channels),
                         nn.Conv3d(in_channels, out_channels, kernel_size=1))


# 2 groups 3dconvTrans(second DW）
def convTrans_3d_dw(in_channels, out_channels, kernel_size, pad, output_pad, stride):
    return nn.Sequential(nn.ConvTranspose3d(in_channels, out_channels, kernel_size=1),
                         nn.ConvTranspose3d(out_channels, out_channels, kernel_size=kernel_size, stride=stride,
                                            padding=pad, output_padding=output_pad, bias=False, groups=out_channels))


# Res
class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, inplanes, planes, stride, downsample, pad, dilation):
        super(BasicBlock, self).__init__()
        # inplanes为输入通道，planes为输出通道，3为卷积核大小
        self.conv1 = nn.Sequential(convbn(inplanes, planes, 3, stride, pad, dilation),
                                   nn.ReLU(inplace=True))
        self.conv2 = convbn(planes, planes, 3, 1, pad, dilation)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        out = self.conv1(x)
        out = self.conv2(out)
        # self.downsample 是一个用于存储下采样函数的变量，并且根据需要可以为 None 或其他函数
        if self.downsample is not None:
            x = self.downsample(x)
        out += x
        return out


class feature_extraction(nn.Module):
    def __init__(self):
        super(feature_extraction, self).__init__()
        self.inplanes = 32
        self.firstconv = nn.Sequential(convbn(3, 32, 3, 2, 1, 1),
                                       nn.ReLU(inplace=True),
                                       convbn(32, 32, 3, 1, 1, 1),
                                       nn.ReLU(inplace=True),
                                       convbn(32, 32, 3, 1, 1, 1),
                                       nn.ReLU(inplace=True))
        # BasicBlock为conv+bn+relu+conv+bn
        self.layer1 = self._make_layer(BasicBlock, 32, 3, 1, 1, 1)
        self.layer2 = self._make_layer(BasicBlock, 64, 16, 2, 1, 1)
        self.layer3 = self._make_layer(BasicBlock, 128, 3, 1, 1, 1)
        self.layer4 = self._make_layer(BasicBlock, 128, 3, 1, 1, 2)
    # 输入通道规定为32
    # block为要构建的基础模块，planes为输出通道，blocks为要构建的block的数量
    def _make_layer(self, block, planes, blocks, stride, pad, dilation):
        # 不进行下采样
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * block.expansion,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(planes * block.expansion), )
        layers = []
        # 初始化block并添加到layers中
        # 只有第一个block进行下采样
        layers.append(block(self.inplanes, planes, stride, downsample, pad, dilation))
        # BasicBlock的expansion=1
        self.inplanes = planes * block.expansion
        # blocks为总的block的数量
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes, 1, None, pad, dilation))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.firstconv(x)
        x = self.layer1(x)
        l2 = self.layer2(x)
        l3 = self.layer3(l2)
        l4 = self.layer4(l3)
        feature = torch.cat((l2, l3, l4), dim=1)
        return feature


class feature_extraction_spp(nn.Module):
    def __init__(self):
        super(feature_extraction_spp, self).__init__()
        self.inplanes = 32
        self.firstconv = nn.Sequential(convbn(3, 32, 3, 2, 1, 1),
                                       nn.ReLU(inplace=True),
                                       convbn(32, 32, 3, 1, 1, 1),
                                       nn.ReLU(inplace=True),
                                       convbn(32, 32, 3, 1, 1, 1),
                                       nn.ReLU(inplace=True))

        self.layer1 = self._make_layer(BasicBlock, 32, 3, 1, 1, 1)
        self.layer2 = self._make_layer(BasicBlock, 64, 16, 2, 1, 1)
        self.layer3 = self._make_layer(BasicBlock, 128, 3, 1, 1, 1)
        self.layer4 = self._make_layer(BasicBlock, 128, 3, 1, 1, 2)

        self.branch1 = nn.Sequential(nn.AvgPool2d((64, 64), stride=(64, 64)),
                                     convbn(128, 32, 1, 1, 0, 1),
                                     nn.ReLU(inplace=True))
        self.branch2 = nn.Sequential(nn.AvgPool2d((32, 32), stride=(32, 32)),
                                     convbn(128, 32, 1, 1, 0, 1),
                                     nn.ReLU(inplace=True))
        self.branch3 = nn.Sequential(nn.AvgPool2d((16, 16), stride=(16, 16)),
                                     convbn(128, 32, 1, 1, 0, 1),
                                     nn.ReLU(inplace=True))
        self.branch4 = nn.Sequential(nn.AvgPool2d((8, 8), stride=(8, 8)),
                                     convbn(128, 32, 1, 1, 0, 1),
                                     nn.ReLU(inplace=True))
        self.lastconv = nn.Sequential(convbn(320, 128, 3, 1, 1, 1),  # 320 = 128(conv4_3)+64(conv2_16)+32*4,,,3x3,128
                                      nn.ReLU(inplace=True),
                                      nn.Conv2d(128, 32, kernel_size=1, padding=0, stride=1, bias=False))  # 1x1,32

    def _make_layer(self, block, planes, blocks, stride, pad, dilation):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * block.expansion,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(planes * block.expansion), )
        layers = []
        layers.append(block(self.inplanes, planes, stride, downsample, pad, dilation))
        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes, 1, None, pad, dilation))
        return nn.Sequential(*layers)

    def forward(self, x):
        output = self.firstconv(x)
        output = self.layer1(output)
        output_raw = self.layer2(output)
        output = self.layer3(output_raw)
        output_skip = self.layer4(output)

        output_branch1 = self.branch1(output_skip)
        output_branch1 = F.upsample(output_branch1, (output_skip.size()[2], output_skip.size()[3]), mode='bilinear')

        output_branch2 = self.branch2(output_skip)
        output_branch2 = F.upsample(output_branch2, (output_skip.size()[2], output_skip.size()[3]), mode='bilinear')

        output_branch3 = self.branch3(output_skip)
        output_branch3 = F.upsample(output_branch3, (output_skip.size()[2], output_skip.size()[3]), mode='bilinear')

        output_branch4 = self.branch4(output_skip)
        output_branch4 = F.upsample(output_branch4, (output_skip.size()[2], output_skip.size()[3]), mode='bilinear')

        output_feature = torch.cat(
            (output_raw, output_skip, output_branch4, output_branch3, output_branch2, output_branch1), 1)
        output_feature = self.lastconv(output_feature)

        return output_feature


class disparityregression(nn.Module):
    def __init__(self, maxdisp):
        super(disparityregression, self).__init__()
        self.disp = torch.Tensor(np.reshape(np.array(range(maxdisp)), [1, maxdisp, 1, 1])).cuda()

    def forward(self, x):
        out = torch.sum(x * self.disp.data, 1, keepdim=True)
        return out


class disparityregression2(nn.Module):
    def __init__(self, start, end, stride=1):
        super(disparityregression2, self).__init__()
        self.disp = torch.arange(start * stride, end * stride, stride, device='cuda', requires_grad=False).view(1, -1,
                                                                                                                1,
                                                                                                                1).float()

    def forward(self, x):
        disp = self.disp.repeat(x.size()[0], 1, x.size()[2], x.size()[3])
        out = torch.sum(x * disp, 1, keepdim=True)
        return out


class CostVolume(nn.Module):
    def __init__(self, max_disp, method):
        super(CostVolume, self).__init__()
        self.max_disp = max_disp
        self.method = method

    def forward(self, left_feature, right_feature):
        B, C, H, W = left_feature.size()

        if self.method == 'concat':
            cost_volume = left_feature.new_zeros(B, 2 * C, self.max_disp, H, W)
            for i in range(self.max_disp):
                if i > 0:
                    cost_volume[:, :, i, :, i:] = torch.cat((left_feature[:, :, :, i:], right_feature[:, :, :, :-i]),
                                                            dim=1)
                else:
                    cost_volume[:, :, i, :, :] = torch.cat((left_feature, right_feature), dim=1)

        elif self.method == 'correlation':
            cost_volume = left_feature.new_zeros(B, self.max_disp, H, W)
            for i in range(self.max_disp):
                if i > 0:
                    cost_volume[:, i, :, i:] = (left_feature[:, :, :, i:] * right_feature[:, :, :, :-i]).mean(dim=1)
                else:
                    cost_volume[:, i, :, :] = (left_feature * right_feature).mean(dim=1)

        elif self.method == 'warp_cost':
            cost_volume = left_feature.new_zeros(B, self.max_disp * 2, H, W)
            for i in range(self.max_disp * 2):
                if i > 0:
                    if i < self.max_disp:
                        cost_volume[:, i, :, :-i] = (left_feature[:, :, :, :-i] * right_feature[:, :, :, i:]).mean(
                            dim=1)
                    elif i == self.max_disp:
                        cost_volume[:, i, :, :] = (left_feature * right_feature).mean(dim=1)
                    elif i > self.max_disp:
                        cost_volume[:, i, :, i:] = (left_feature[:, :, :, i:] * right_feature[:, :, :, :-i]).mean(dim=1)
                else:
                    cost_volume[:, i, :, :] = (left_feature * right_feature).mean(dim=1)

        else:
            raise NotImplementedError

        cost_volume = cost_volume.contiguous()
        return cost_volume


class CBAMLayer(nn.Module):
    def __init__(self, channel, reduction=8, spatial_kernel=3):
        super(CBAMLayer, self).__init__()
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.avg_pool = nn.AdaptiveAvgPool2d(1)

        self.mlp = nn.Sequential(
            nn.Conv2d(channel, channel // reduction, 1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(channel // reduction, channel, 1, bias=False)
        )
        # spatial attention
        self.conv = nn.Conv2d(2, 1, kernel_size=spatial_kernel,
                              padding=spatial_kernel // 2, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        max_out = self.mlp(self.max_pool(x))
        avg_out = self.mlp(self.avg_pool(x))
        channel_out = self.sigmoid(max_out + avg_out)
        x = channel_out * x
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        avg_out = torch.mean(x, dim=1, keepdim=True)
        spatial_out = self.sigmoid(self.conv(torch.cat([max_out, avg_out], dim=1)))
        x = spatial_out * x
        return x


class CAMLayer(nn.Module):
    def __init__(self, channel, reduction=2):
        super(CAMLayer, self).__init__()
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.avg_pool = nn.AdaptiveAvgPool2d(1)

        self.mlp = nn.Sequential(
            nn.Conv2d(channel, channel // reduction, 1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(channel // reduction, channel, 1, bias=False)
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        max_out = self.mlp(self.max_pool(x))
        avg_out = self.mlp(self.avg_pool(x))
        channel_out = self.sigmoid(max_out + avg_out)
        x = channel_out * x
        return x


class SAMLayer(nn.Module):
    def __init__(self, spatial_kernel=1):
        super(SAMLayer, self).__init__()
        # spatial attention
        self.conv = nn.Conv2d(2, 1, kernel_size=spatial_kernel,
                              padding=0, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        avg_out = torch.mean(x, dim=1, keepdim=True)
        spatial_out = self.sigmoid(self.conv(torch.cat([max_out, avg_out], dim=1)))
        x = spatial_out * x
        return x


class attention_block_3d(nn.Module):
    def __init__(self, channels_3d, num_heads=8, block=4):
        """
        ws 1 for stand attention
        """
        super(attention_block_3d, self).__init__()
        self.block = block
        self.dim_3d = channels_3d
        self.num_heads = num_heads
        head_dim_3d = self.dim_3d // num_heads
        self.scale_3d = head_dim_3d ** -0.5
        self.qkv_3d = nn.Linear(self.dim_3d, self.dim_3d * 3, bias=True)
        self.final1x1 = torch.nn.Conv3d(self.dim_3d, self.dim_3d, 1)

    def forward(self, x):

        B, C, D, H0, W0 = x.shape
        pad_l = pad_t = 0
        pad_r = (self.block[2] - W0 % self.block[2]) % self.block[2]
        pad_b = (self.block[1] - H0 % self.block[1]) % self.block[1]
        x = F.pad(x, (pad_l, pad_r, pad_t, pad_b))
        B, C, D, H, W = x.shape
        d, h, w = D // self.block[0], H // self.block[1], W // self.block[2]

        x = x.view(B, C, d, self.block[0], h, self.block[1], w, self.block[2]).permute(0, 2, 4, 6, 3, 5, 7, 1)

        qkv_3d = self.qkv_3d(x).reshape(B, d * h * w, self.block[0] * self.block[1] * self.block[2], 3, self.num_heads,
                                        C // self.num_heads).permute(3, 0, 1, 4, 2,
                                                                     5)  # [3,B,d*h*w,num_heads,blocks,C//num_heads]
        q_3d, k_3d, v_3d = qkv_3d[0], qkv_3d[1], qkv_3d[2]
        attn = (q_3d @ k_3d.transpose(-2, -1)) * self.scale_3d
        if pad_r > 0 or pad_b > 0:
            mask = torch.zeros((1, H, W), device=x.device)
            mask[:, -pad_b:, :].fill_(1)
            mask[:, :, -pad_r:].fill_(1)
            mask = mask.reshape(1, h, self.block[1], w, self.block[2]).transpose(2, 3).reshape(1, h * w, self.block[1] *
                                                                                               self.block[2])
            attn_mask = mask.unsqueeze(2) - mask.unsqueeze(3)  # 1, _h*_w, self.block*self.block, self.block*self.block
            attn_mask = attn_mask.masked_fill(attn_mask != 0, float(-1000.0)).masked_fill(attn_mask == 0, float(0.0))
            attn = attn + attn_mask.repeat(1, d, self.block[0], self.block[0]).unsqueeze(2)

        attn = torch.softmax(attn, dim=-1)

        x = (attn @ v_3d).view(B, d, h, w, self.num_heads, self.block[0], self.block[1], self.block[2], -1).permute(0,
                                                                                                                    4,
                                                                                                                    8,
                                                                                                                    1,
                                                                                                                    5,
                                                                                                                    2,
                                                                                                                    6,
                                                                                                                    3,
                                                                                                                    7)
        x = x.reshape(B, C, D, H, W)
        if pad_r > 0 or pad_b > 0:
            x = x[:, :, :, :H0, :W0]
        return self.final1x1(x)


class FeaturePyramidNetwork(nn.Module):
    def __init__(self, in_channels, out_channels=128,
                 num_levels=3):
        # FPN paper uses 256 out channels by default
        super(FeaturePyramidNetwork, self).__init__()

        assert isinstance(in_channels, list)

        self.in_channels = in_channels

        self.lateral_convs = nn.ModuleList()
        self.fpn_convs = nn.ModuleList()

        for i in range(num_levels):
            lateral_conv = nn.Conv2d(in_channels[i], out_channels, 1)
            fpn_conv = nn.Sequential(
                nn.Conv2d(out_channels, out_channels, 3, padding=1),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(inplace=True))

            self.lateral_convs.append(lateral_conv)
            self.fpn_convs.append(fpn_conv)

        # Initialize weights
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.xavier_uniform_(m.weight, gain=1)
                if hasattr(m, 'bias'):
                    nn.init.constant_(m.bias, 0)

    def forward(self, inputs):
        # Inputs: resolution high  -> low
        assert len(self.in_channels) == len(inputs)

        # Build laterals
        laterals = [lateral_conv(inputs[i])
                    for i, lateral_conv in enumerate(self.lateral_convs)]

        # Build top-down path
        used_backbone_levels = len(laterals)
        for i in range(used_backbone_levels - 1, 0, -1):
            laterals[i - 1] += F.interpolate(
                laterals[i], scale_factor=2, mode='nearest')

        # Build outputs
        out = [
            self.fpn_convs[i](laterals[i]) for i in range(used_backbone_levels)
        ]

        return out


class FeaturePyrmaid(nn.Module):
    def __init__(self, in_channel=32):
        super(FeaturePyrmaid, self).__init__()
        self.out1 = nn.Sequential(nn.Conv2d(in_channel, in_channel * 2, kernel_size=3,
                                            stride=2, padding=1, bias=False),
                                  nn.BatchNorm2d(in_channel * 2),
                                  nn.LeakyReLU(0.2, inplace=True),
                                  nn.Conv2d(in_channel * 2, in_channel * 2, kernel_size=1,
                                            stride=1, padding=0, bias=False),
                                  nn.BatchNorm2d(in_channel * 2),
                                  nn.LeakyReLU(0.2, inplace=True),
                                  )
        self.out2 = nn.Sequential(nn.Conv2d(in_channel * 2, in_channel * 4, kernel_size=3,
                                            stride=2, padding=1, bias=False),
                                  nn.BatchNorm2d(in_channel * 4),
                                  nn.LeakyReLU(0.2, inplace=True),
                                  nn.Conv2d(in_channel * 4, in_channel * 4, kernel_size=1,
                                            stride=1, padding=0, bias=False),
                                  nn.BatchNorm2d(in_channel * 4),
                                  nn.LeakyReLU(0.2, inplace=True),
                                  )

    def forward(self, x):
        # x: [B, 32, H, W]
        out1 = self.out1(x)  # [B, 64, H/2, W/2]
        out2 = self.out2(out1)  # [B, 128, H/4, W/4]

        return x, out1, out2

class MySobelx(nn.Module):
    def __init__(self):
        super(MySobelx, self).__init__()
        self.sobel_x = torch.tensor([[-1.0, 0, 1.0],
                                     [-2.0, 0, 2.0],
                                     [-1.0, 0, 1.0]], dtype=torch.float, requires_grad=False).view(1, 1, 3, 3).cuda()
        # self.sobel_y = torch.tensor([[-1.0, -2.0, -1.0],
        #                              [0, 0, 0],
        #                              [1.0, 2.0, 1.0]], dtype=torch.float, requires_grad=False).view(1, 1, 3, 3).cuda()
    # 使用 F.conv2d对输入x进行卷积操作，卷积核使用sobel_x重复扩展到与输入的通道数一致。
    def forward(self, x):
        out_x = F.conv2d(x, self.sobel_x.repeat(1, x.size(1), 1, 1), stride=1, padding=1)
        # out_y = F.conv2d(x, self.sobel_y.repeat(1, x.size(1), 1, 1), stride=1, padding=1)
        # out = 0.5 * out_x + 0.5 * out_y
        out = out_x
        return out

class deform_aggre(nn.Module):
    def __init__(self, in_channels):
        super(deform_aggre, self).__init__()
        # self.conv1 = nn.Sequential(convDeform_bn(in_channels, in_channels, (3, 3), (1, 1), 1),
        #                            nn.ReLU(inplace=True))
        self.CAMmodel = CAMLayer(in_channels)
        # self.conv2 = nn.Sequential(convDeform_bn(in_channels, in_channels, (3, 3), (1, 1), 1),
        #                            nn.ReLU(inplace=True))

    def forward(self, myinput):
        output1 = self.conv1(myinput)
        output2 = self.conv2(output1)
        output3 = self.CAMmodel(output2)
        return output3


# hg+cbam
class hourglass_2d_cbam(nn.Module):
    def __init__(self, in_channels):
        super(hourglass_2d_cbam, self).__init__()
        self.conv1 = nn.Sequential(convbn(in_channels, in_channels * 2, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv2 = nn.Sequential(convbn(in_channels * 2, in_channels * 2, 3, 1, 1),
                                   nn.ReLU(inplace=True))
        self.conv3 = nn.Sequential(convbn(in_channels * 2, in_channels * 4, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv4 = convbn(in_channels * 4, in_channels * 4, 3, 1, 1)
        self.conv5 = convTrans_bn(in_channels * 4, in_channels * 2, 3, 2, 1, 1)
        self.conv6 = convTrans_bn(in_channels * 2, in_channels, 3, 2, 1, 1)

        self.ShortCut1 = convbn(in_channels, in_channels, 1, 1, 0)
        self.ShortCut2 = convbn(in_channels * 2, in_channels * 2, 1, 1, 0)
        self.CBAMmodel = CBAMLayer(in_channels * 4)

    def forward(self, myinput):
        output1 = self.conv1(myinput)
        output2 = self.conv2(output1)
        output3 = self.conv3(output2)

        output4 = F.relu(self.conv4(output3) + self.CBAMmodel(output3), inplace=True)
        # output4 = self.conv4(output3)

        output5 = F.relu(
            F.upsample(self.conv5(output4), (output2.size(2), output2.size(3)), mode='bilinear') + self.ShortCut2(
                output2), inplace=True)
        output6 = F.relu(
            F.upsample(self.conv6(output5), (myinput.size(2), myinput.size(3)), mode='bilinear') + self.ShortCut1(
                myinput), inplace=True)
        return output6

# 沙漏网络调用CBAMLayer时，需要设置好通道的压缩比例，如果输入通道数小于压缩比例会报“除0”错误
class hourglass_2d_cbam_sigmoid(nn.Module):
    def __init__(self, in_channels):
        super(hourglass_2d_cbam_sigmoid, self).__init__()
        self.conv1 = nn.Sequential(convbn(in_channels, in_channels * 2, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv2 = nn.Sequential(convbn(in_channels * 2, in_channels * 2, 3, 1, 1),
                                   nn.ReLU(inplace=True))
        self.conv3 = nn.Sequential(convbn(in_channels * 2, in_channels * 4, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv4 = convbn(in_channels * 4, in_channels * 4, 3, 1, 1)
        self.conv5 = convTrans_bn(in_channels * 4, in_channels * 2, 3, 2, 1, 1)
        self.conv6 = convTrans_bn(in_channels * 2, in_channels, 3, 2, 1, 1)

        self.ShortCut1 = convbn(in_channels, in_channels, 1, 1, 0)
        self.ShortCut2 = convbn(in_channels * 2, in_channels * 2, 1, 1, 0)
        self.CBAMmodel = CBAMLayer(in_channels * 4)

    def forward(self, myinput):
        output1 = self.conv1(myinput)
        output2 = self.conv2(output1)
        output3 = self.conv3(output2)

        output4 = F.relu(self.conv4(output3) + self.CBAMmodel(output3), inplace=True)
        # output4 = self.conv4(output3)

        output5 = F.relu(
            F.upsample(self.conv5(output4), (output2.size(2), output2.size(3)), mode='bilinear') + self.ShortCut2(
                output2), inplace=True)
        output6 = F.sigmoid(
            F.upsample(self.conv6(output5), (myinput.size(2), myinput.size(3)), mode='bilinear') + self.ShortCut1(
                myinput))
        return output6

# HG+CAM+SAM(先SAM再CAM)
class hourglass_2d_cam_sam(nn.Module):
    def __init__(self, in_channels):
        super(hourglass_2d_cam_sam, self).__init__()
        self.conv1 = nn.Sequential(convbn(in_channels, in_channels * 2, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv2 = nn.Sequential(convbn(in_channels * 2, in_channels * 2, 3, 1, 1),
                                   nn.ReLU(inplace=True))
        self.conv3 = nn.Sequential(convbn(in_channels * 2, in_channels * 4, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv4 = convbn(in_channels * 4, in_channels * 4, 3, 1, 1)
        self.conv5 = convTrans_bn(in_channels * 4, in_channels * 2, 3, 2, 1, 1)
        self.conv6 = convTrans_bn(in_channels * 2, in_channels, 3, 2, 1, 1)

        self.ShortCut1 = convbn(in_channels, in_channels, 1, 1, 0)
        self.ShortCut2 = convbn(in_channels * 2, in_channels * 2, 1, 1, 0)
        self.CAMmodel = CAMLayer(in_channels, reduction=4)
        self.SAMmodel = SAMLayer()

    def forward(self, myinput):
        output1 = self.conv1(myinput)
        output2 = self.conv2(output1)
        output3 = self.conv3(output2)

        output4 = F.relu(self.conv4(output3) + self.SAMmodel(output3), inplace=True)
        # output4 = self.conv4(output3)

        output5 = F.relu(
            F.upsample(self.conv5(output4), (output2.size(2), output2.size(3)), mode='bilinear') + self.ShortCut2(
                output2), inplace=True)
        output6 = F.relu(
            F.upsample(self.conv6(output5), (myinput.size(2), myinput.size(3)), mode='bilinear') + self.ShortCut1(
                myinput), inplace=True)
        output7 = self.CAMmodel(output6)
        return output7


# hg+cam
class hourglass_2d_cam(nn.Module):
    def __init__(self, in_channels):
        super(hourglass_2d_cam, self).__init__()
        self.conv1 = nn.Sequential(convbn(in_channels, in_channels * 2, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv2 = nn.Sequential(convbn(in_channels * 2, in_channels * 2, 3, 1, 1),
                                   nn.ReLU(inplace=True))
        self.conv3 = nn.Sequential(convbn(in_channels * 2, in_channels * 4, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv4 = convbn(in_channels * 4, in_channels * 4, 3, 1, 1)
        self.conv5 = convTrans_bn(in_channels * 4, in_channels * 2, 3, 2, 1, 1)
        self.conv6 = convTrans_bn(in_channels * 2, in_channels, 3, 2, 1, 1)

        self.ShortCut1 = convbn(in_channels, in_channels, 1, 1, 0)
        self.ShortCut2 = convbn(in_channels * 2, in_channels * 2, 1, 1, 0)
        self.CAMmodel = CAMLayer(in_channels * 4)

    def forward(self, myinput):
        output1 = self.conv1(myinput)
        output2 = self.conv2(output1)
        output3 = self.conv3(output2)

        output4 = F.relu(self.conv4(output3) + self.CAMmodel(output3), inplace=True)
        # output4 = self.conv4(output3)

        output5 = F.relu(
            F.upsample(self.conv5(output4), (output2.size(2), output2.size(3)), mode='bilinear') + self.ShortCut2(
                output2), inplace=True)
        output6 = F.relu(
            F.upsample(self.conv6(output5), (myinput.size(2), myinput.size(3)), mode='bilinear') + self.ShortCut1(
                myinput), inplace=True)
        return output6


# hg+sam
class hourglass_2d_sam(nn.Module):
    def __init__(self, in_channels):
        super(hourglass_2d_sam, self).__init__()
        self.conv1 = nn.Sequential(convbn(in_channels, in_channels * 2, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv2 = nn.Sequential(convbn(in_channels * 2, in_channels * 2, 3, 1, 1),
                                   nn.ReLU(inplace=True))
        self.conv3 = nn.Sequential(convbn(in_channels * 2, in_channels * 4, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv4 = convbn(in_channels * 4, in_channels * 4, 3, 1, 1)
        self.conv5 = convTrans_bn(in_channels * 4, in_channels * 2, 3, 2, 1, 1)
        self.conv6 = convTrans_bn(in_channels * 2, in_channels, 3, 2, 1, 1)

        self.ShortCut1 = convbn(in_channels, in_channels, 1, 1, 0)
        self.ShortCut2 = convbn(in_channels * 2, in_channels * 2, 1, 1, 0)
        self.SAMmodel = SAMLayer()

    def forward(self, myinput):
        output1 = self.conv1(myinput)
        output2 = self.conv2(output1)
        output3 = self.conv3(output2)

        output4 = F.relu(self.conv4(output3) + self.SAMmodel(output3), inplace=True)
        # output4 = self.conv4(output3)

        output5 = F.relu(
            F.upsample(self.conv5(output4), (output2.size(2), output2.size(3)), mode='bilinear') + self.ShortCut2(
                output2), inplace=True)
        output6 = F.relu(
            F.upsample(self.conv6(output5), (myinput.size(2), myinput.size(3)), mode='bilinear') + self.ShortCut1(
                myinput), inplace=True)
        return output6


# only hg
class hourglass_2d(nn.Module):
    def __init__(self, in_channels):
        super(hourglass_2d, self).__init__()
        self.conv1 = nn.Sequential(convbn(in_channels, in_channels * 2, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv2 = nn.Sequential(convbn(in_channels * 2, in_channels * 2, 3, 1, 1),
                                   nn.ReLU(inplace=True))
        self.conv3 = nn.Sequential(convbn(in_channels * 2, in_channels * 4, 3, 2, 1),
                                   nn.ReLU(inplace=True))
        self.conv4 = nn.Sequential(convbn(in_channels * 4, in_channels * 4, 3, 1, 1),
                                   nn.ReLU(inplace=True))
        self.conv5 = convTrans_bn(in_channels * 4, in_channels * 2, 3, 2, 1, 1)
        self.conv6 = convTrans_bn(in_channels * 2, in_channels, 3, 2, 1, 1)

        self.ShortCut1 = convbn(in_channels, in_channels, 1, 1, 0)
        self.ShortCut2 = convbn(in_channels * 2, in_channels * 2, 1, 1, 0)

    def forward(self, myinput):
        output1 = self.conv1(myinput)
        output2 = self.conv2(output1)
        output3 = self.conv3(output2)
        output4 = self.conv4(output3)
        output5 = F.relu(
            F.upsample(self.conv5(output4), (output2.size(2), output2.size(3)), mode='bilinear') + self.ShortCut2(
                output2), inplace=True)
        output6 = F.relu(
            F.upsample(self.conv6(output5), (myinput.size(2), myinput.size(3)), mode='bilinear') + self.ShortCut1(
                myinput), inplace=True)
        return output6