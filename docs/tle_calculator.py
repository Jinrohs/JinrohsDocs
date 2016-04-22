# -*- coding: utf-8 -*-

from math import sin, cos, acos, sqrt, pi
import time


class TLECalculator:
    """  """

    # ---- 物理定数 ----
    # 万有引力定数 * 地球質量 [km^3/day^2]
    GM = 2.975537e15
    # 地球半径 [km]
    radius = 6.378137e3
    

    def __init__(self, tle):
        self.tle = {}
        self.update_params(tle)
        # パラメータ諸々を計算

    def update_params(self, tle):
        # get parameters from response JSON
        #object_type = tle["OBJECT_TYPE"]
        self.tle["epoch"] = int(time.mktime(time.strptime(tle["EPOCH"], "%Y-%m-%d %H:%M:%S")))  # 元期(Unix Time)
        self.tle["eccentricity"] = float(tle["ECCENTRICITY"])  # 楕円軌道の離心率
        self.tle["mean_motion"] = float(tle["MEAN_MOTION"])  # 平均運動(周/day)
        self.tle["mean_motion_dot"] = float(tle["MEAN_MOTION_DOT"])  # 平均運動変化係数
        self.tle["mean_anomaly"] = float(tle["MEAN_ANOMALY"])  # 平均近点角
        self.tle["inclination"] = float(tle["INCLINATION"])  # 軌道傾斜角
        self.tle["arg_of_perigee"] = float(tle["ARG_OF_PERICENTER"])  # 近地点引数
        self.tle["ra_of_asc_node"] = float(tle["RA_OF_ASC_NODE"])  # 昇交点赤経

        
    def calculate_ra_dec(self, unix_time):
        # mean_motion は時事刻々と変わるので、毎回計算したほうがいいかも
        # mean_motion = mean_motion_0 + mean_motion_dot * dt(=今の時刻-epoch)

        e = self.tle["eccentricity"]
        mean_motion = self.tle["mean_motion"]
        mean_motion_dot = self.tle["mean_motion_dot"]
        mean_anomaly = self.tle["mean_anomaly"]


        # 元期からの経過日数
        dt = (unix_time - self.tle["epoch"]) / 86400.0
        print "元期からの経過日数（合ってる）", dt

        # ほんの少し変わるかも？
        mean_motion = mean_motion + dt*mean_motion_dot
        
        # 楕円軌道の長半径
        a = (self.GM/(4*pi*pi*mean_motion*mean_motion)) ** (1/3.0)
        print "軌道長半径[km]", a
        # 観測時の平均近点角[地球の回転数(rev), ラジアン(rad)]
        M_rev = mean_anomaly/360 + mean_motion * dt + mean_motion_dot*0.5*dt*dt
        print M_rev, M_rev-int(M_rev)
        M_rad = self.degree_to_rad((M_rev - int(M_rev)) * 360)
        # 離心近点角 [rad]
        E = self.calculate_eccentric_anomaly(M_rad, e)

        # 真の
        

        U = a * cos(E) - a * e
        V = a * sqrt(1 - e * e) * sin(E)

        i = self.tle["inclination"]
        ap_0 = self.tle["arg_of_perigee"]
        raan_0 = self.tle["ra_of_asc_node"]

        # 2回使う定数
        c = pi*(a/self.radius)**3.5
        # 近地点引数 [rad]
        ap = self.degree_to_rad(ap_0 + 180*0.174*(2-2.5*sin(i)*sin(i))/c * dt)
        # 昇交点赤経 [rad]
        raan = self.degree_to_rad(raan_0 - 180*0.174*cos(i)/c * dt)

        # 2010/01/01 00:00:00 のグリニッジ恒星時 [rad] <- 理科年表より
        #   cf. グリニッジ恒星時 = 春分点の方向とグリニッジ（greenwich）子午線との角度差
        theta_gw_0 = 0.27928240740740745 * 2 * pi
        # 基準時 2010/01/01 00:00:00 の unix time [s]
        t0_gw = int(time.mktime(time.strptime("2010-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")))
        # 指定時刻のグリニッジ恒星時 [地球の回転数 (rev)]
        theta_gw = 0.27928240740740745 + 1.002737909 * (unix_time - t0_gw) / 86400.0
        # 指定時刻のグリニッジ恒星時 [rad]
        theta_gw = (theta_gw - int(theta_gw)) * 2 * pi

        # 合ってそう
        # http://eco.mtk.nao.ac.jp/cgi-bin/koyomi/cande/gst.cgi
        print "グリニッジ恒星時(hour)", theta_gw/pi*12

        s_i, c_i = sin(i), cos(i)
        s_ap, c_ap = sin(ap), cos(ap)
        # raan だけだと x 軸が春分点を向いた座標系になってしまう（地球が動く）
        # 地球静止系に直すため、春分点と グリニッジ子午線がなす角度も補正する
        s_raan_gw, c_raan_gw = sin(raan - theta_gw), cos(raan - theta_gw)

        x = (c_raan_gw*c_ap-s_raan_gw*c_i*s_ap) * U + (-c_raan_gw*s_ap-s_raan_gw*c_i*c_ap) * V
        y = (s_raan_gw*c_ap-c_raan_gw*c_i*s_ap) * U + (-s_raan_gw*s_ap-c_raan_gw*c_i*c_ap) * V
        z = s_i*s_ap*U + c_i*c_ap*V

        print x, y, z

        r, theta, phi = self.cartesian_to_polar(x, y, z)

        print "r, 緯度, 経度", r, 90-theta*180/pi, phi*180/pi-180


    def degree_to_rad(self, degree):
        return degree * pi / 180


    def cartesian_to_polar(self, x, y, z):
        r = sqrt(x*x + y*y + z*z)
        theta = acos(z / r)
        # acos は [0, pi] の範囲の値しか返さないため、第3象限 or 第4象限に
        # ある場合は補正が必要
        phi_tmp = acos(x / sqrt(x*x + y*y))
        if y < 0:
            phi = 2*pi - phi_tmp
        else:
            phi = phi_tmp
        return (r, theta, phi)


    def calculate_eccentric_anomaly(self, M, e):
        """
        M (観測時の平均近点角) と e (離心率) から離心近点角を求める
        """
        epsilon = 0.000001
        def f(E):
            return M - E + e * sin(E)
        def df_over_dE(E):
            return e * cos(E) - 1
        E = pi
        E_old = E
        cnt = 0
        while cnt < 100:
            E = E - f(E) / df_over_dE(E)
            if E - E_old < epsilon:
                break
            E_old = E
            cnt += 1
        return E


        
